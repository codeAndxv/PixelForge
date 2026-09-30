<script setup lang="ts">
import type { TabMode } from '../../types';
import ThemeToggle from '../common/ThemeToggle.vue';

defineProps<{
  currentTab: TabMode;
}>();

const emit = defineEmits<{
  (e: 'update:currentTab', tab: TabMode): void;
}>();
</script>

<template>
  <header class="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur sticky top-0 z-30 px-6 py-3.5 flex items-center justify-between shadow-xs dark:shadow-none">
    <!-- 品牌 Logo 与标题 -->
    <div class="flex items-center space-x-3">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/20 font-black text-lg text-white">
        PF
      </div>
      <div>
        <h1 class="text-base font-bold tracking-tight bg-gradient-to-r from-slate-900 via-slate-700 to-slate-500 dark:from-white dark:via-slate-200 dark:to-slate-400 bg-clip-text text-transparent">
          PixelForge
        </h1>
        <p class="text-xs text-slate-500 dark:text-slate-400">智能图像矢量化 (SVG) 与 Web 极速压缩 (WebP)</p>
      </div>
    </div>

    <!-- Tab 模式切换 -->
    <div class="flex bg-slate-100 dark:bg-slate-800/90 p-1 rounded-xl border border-slate-200/80 dark:border-slate-700/60 shadow-inner">
      <button
        @click="emit('update:currentTab', 'svg')"
        :class="currentTab === 'svg' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200'"
        class="flex items-center space-x-2 px-4 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer">
        <span>📐</span>
        <span>转 SVG 矢量图</span>
      </button>
      <button
        @click="emit('update:currentTab', 'webp')"
        :class="currentTab === 'webp' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200'"
        class="flex items-center space-x-2 px-4 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer">
        <span>🗜️</span>
        <span>转 WebP 压缩</span>
      </button>
    </div>

    <!-- 右侧工具栏：运行状态与主题切换 -->
    <div class="flex items-center space-x-3">
      <div class="hidden sm:flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800/50 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800">
        <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="font-medium">API Core Active</span>
      </div>

      <!-- 白天 / 黑夜切换按钮 -->
      <ThemeToggle />
    </div>
  </header>
</template>
