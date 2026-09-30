<script setup lang="ts">
import type { WebpParams } from '../../types';

const props = defineProps<{
  params: WebpParams;
}>();

const emit = defineEmits<{
  (e: 'update:params', params: WebpParams): void;
  (e: 'change'): void;
}>();

function updateField<K extends keyof WebpParams>(key: K, value: WebpParams[K]) {
  const updated = { ...props.params, [key]: value };
  emit('update:params', updated);
  emit('change');
}
</script>

<template>
  <div class="space-y-4 text-xs">
    <!-- 纯无损模式 -->
    <div class="flex items-center justify-between p-3 bg-slate-100 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700/50">
      <div>
        <div class="font-bold text-slate-800 dark:text-slate-200">纯无损模式 (Lossless)</div>
        <div class="text-[10px] text-slate-500 dark:text-slate-400">100% 像素点还原，体积减少 ~30%</div>
      </div>
      <input
        type="checkbox"
        :checked="params.lossless"
        @change="(e) => updateField('lossless', (e.target as HTMLInputElement).checked)"
        class="w-4 h-4 accent-indigo-600 rounded cursor-pointer" />
    </div>

    <!-- 压缩质量滑块 -->
    <div v-if="!params.lossless" class="space-y-1">
      <div class="flex justify-between text-slate-600 dark:text-slate-400">
        <span>压缩质量 (Quality)</span>
        <span class="text-indigo-600 dark:text-indigo-400 font-mono font-bold">{{ params.quality }} %</span>
      </div>
      <input
        type="range"
        min="1"
        max="100"
        step="1"
        :value="params.quality"
        @input="(e) => updateField('quality', Number((e.target as HTMLInputElement).value))"
        class="w-full accent-indigo-600 h-1.5 bg-slate-200 dark:bg-slate-800 rounded-lg cursor-pointer" />
      <div class="flex justify-between text-[10px] text-slate-400 dark:text-slate-500">
        <span>极限压缩 (小体积)</span>
        <span>推荐 80% (视觉无损)</span>
        <span>极高质量 (大体积)</span>
      </div>
    </div>

    <!-- 尺寸缩放限制 -->
    <div class="grid grid-cols-2 gap-3">
      <div>
        <label class="block text-slate-600 dark:text-slate-400 mb-1">最大宽度限制 (px)</label>
        <input
          type="number"
          placeholder="保持原宽"
          :value="params.max_width ?? ''"
          @input="(e) => {
            const v = (e.target as HTMLInputElement).value;
            updateField('max_width', v ? Number(v) : null);
          }"
          class="w-full bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
      </div>
      <div>
        <label class="block text-slate-600 dark:text-slate-400 mb-1">最大高度限制 (px)</label>
        <input
          type="number"
          placeholder="保持原高"
          :value="params.max_height ?? ''"
          @input="(e) => {
            const v = (e.target as HTMLInputElement).value;
            updateField('max_height', v ? Number(v) : null);
          }"
          class="w-full bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
      </div>
    </div>
  </div>
</template>
