<script setup lang="ts">
import { ref, computed } from 'vue';
import type { TabMode } from '../../types';

const props = defineProps<{
  currentTab: TabMode;
  currentFile: File | null;
  originalPreviewUrl: string;
  originalSize: number;
  outputSize: number;
  durationMs: number;
  isProcessing: boolean;
  resultSvg: string;
  resultWebpUri: string;
}>();

const copyBtnText = ref('📋 复制代码');

const sizeChangeRatioStr = computed(() => {
  if (!props.originalSize || !props.outputSize) return '';
  const diff = ((props.outputSize - props.originalSize) / props.originalSize) * 100;
  if (diff < 0) {
    return `体积减少 ${Math.abs(diff).toFixed(1)}%`;
  } else {
    return `体积增加 ${diff.toFixed(1)}%`;
  }
});

function formatSize(bytes: number): string {
  if (!bytes) return '0 B';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

function downloadSvg() {
  if (!props.resultSvg) return;
  const blob = new Blob([props.resultSvg], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const baseName = props.currentFile ? props.currentFile.name.replace(/\.[^/.]+$/, '') : 'pixelforge_output';
  a.href = url;
  a.download = `${baseName}.svg`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function copySvgCode() {
  if (!props.resultSvg) return;
  navigator.clipboard.writeText(props.resultSvg).then(() => {
    copyBtnText.value = '✅ 已复制!';
    setTimeout(() => {
      copyBtnText.value = '📋 复制代码';
    }, 2000);
  });
}

function downloadWebp() {
  if (!props.resultWebpUri) return;
  const a = document.createElement('a');
  const baseName = props.currentFile ? props.currentFile.name.replace(/\.[^/.]+$/, '') : 'pixelforge_output';
  a.href = props.resultWebpUri;
  a.download = `${baseName}.webp`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
</script>

<template>
  <div class="flex-1 flex flex-col space-y-5">
    <!-- 未上传图片时的占位区域 -->
    <div
      v-if="!currentFile"
      class="flex-1 bg-white/60 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800/80 rounded-2xl p-12 flex flex-col items-center justify-center text-center space-y-4 min-h-[420px] shadow-xs dark:shadow-none">
      <div class="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800/80 text-slate-500 dark:text-slate-400 flex items-center justify-center text-3xl">
        🖼️
      </div>
      <div class="space-y-1">
        <h3 class="text-base font-bold text-slate-800 dark:text-slate-300">等待上传图片</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 max-w-sm">
          从左侧上传一张 PNG / JPG 图片，即可在此实时查看转换对比与体积优化效果。
        </p>
      </div>
    </div>

    <!-- 已上传：左右分屏对比卡片 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
      <!-- 原图卡片 -->
      <div class="bg-white/80 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 flex flex-col space-y-3 shadow-sm dark:shadow-xl">
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
          <span class="text-xs font-bold text-slate-600 dark:text-slate-400">原始图片 (Bitmap)</span>
          <span class="text-[11px] font-mono text-slate-700 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded border border-slate-200 dark:border-transparent">
            {{ formatSize(originalSize) }}
          </span>
        </div>
        <div class="flex-1 min-h-[240px] max-h-[380px] checkerboard rounded-xl flex items-center justify-center p-3 overflow-hidden border border-slate-200 dark:border-slate-800">
          <img :src="originalPreviewUrl" class="max-w-full max-h-[340px] object-contain shadow-md rounded" />
        </div>
        <div class="text-[11px] text-slate-500 dark:text-slate-400 truncate font-mono">
          {{ currentFile.name }}
        </div>
      </div>

      <!-- 转换产物卡片 -->
      <div class="bg-white/80 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 flex flex-col space-y-3 shadow-sm dark:shadow-xl relative">
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
          <span class="text-xs font-bold text-indigo-600 dark:text-indigo-400">
            {{ currentTab === 'svg' ? '生成的 SVG 矢量图' : '压缩后的 WebP' }}
          </span>

          <!-- 体积与耗时 Badge -->
          <div class="flex items-center space-x-2">
            <span v-if="outputSize > 0" class="text-[11px] font-mono text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 px-2 py-0.5 rounded font-bold">
              {{ formatSize(outputSize) }}
              <span v-if="sizeChangeRatioStr" class="text-[10px] ml-1">({{ sizeChangeRatioStr }})</span>
            </span>
          </div>
        </div>

        <!-- 预览区 -->
        <div class="flex-1 min-h-[240px] max-h-[380px] checkerboard rounded-xl flex items-center justify-center p-3 overflow-hidden border border-slate-200 dark:border-slate-800 relative">
          <!-- 加载中遮罩 -->
          <div v-if="isProcessing" class="absolute inset-0 bg-white/70 dark:bg-slate-950/70 backdrop-blur-xs flex flex-col items-center justify-center z-10 space-y-2">
            <div class="w-6 h-6 border-2 border-indigo-600 dark:border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            <span class="text-xs text-indigo-700 dark:text-indigo-300 font-medium">转换中...</span>
          </div>

          <!-- SVG 渲染 -->
          <div
            v-if="currentTab === 'svg' && resultSvg"
            v-html="resultSvg"
            class="w-full h-full flex items-center justify-center [&>svg]:max-w-full [&>svg]:max-h-[340px] [&>svg]:w-auto [&>svg]:h-auto">
          </div>

          <!-- WebP 渲染 -->
          <img
            v-else-if="currentTab === 'webp' && resultWebpUri"
            :src="resultWebpUri"
            class="max-w-full max-h-[340px] object-contain shadow-md rounded" />

          <div v-else-if="!isProcessing" class="text-xs text-slate-500 dark:text-slate-400">
            点击左侧“执行转换”生成结果
          </div>
        </div>

        <!-- 底部操作按钮 -->
        <div class="flex items-center space-x-2 pt-1">
          <button
            v-if="currentTab === 'svg' && resultSvg"
            @click="downloadSvg"
            class="flex-1 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs rounded-lg transition-all flex items-center justify-center space-x-1 shadow cursor-pointer">
            <span>📥</span>
            <span>下载 SVG</span>
          </button>
          <button
            v-if="currentTab === 'svg' && resultSvg"
            @click="copySvgCode"
            class="px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white text-xs rounded-lg transition-all border border-slate-200 dark:border-slate-700 cursor-pointer">
            {{ copyBtnText }}
          </button>

          <button
            v-if="currentTab === 'webp' && resultWebpUri"
            @click="downloadWebp"
            class="flex-1 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs rounded-lg transition-all flex items-center justify-center space-x-1 shadow cursor-pointer">
            <span>📥</span>
            <span>下载 WebP 图片</span>
          </button>

          <span v-if="durationMs > 0" class="text-[10px] text-slate-500 dark:text-slate-400 font-mono pl-2">
            ⚡ {{ durationMs }} ms
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
