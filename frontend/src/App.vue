<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import Header from './components/layout/Header.vue';
import DropZone from './components/workspace/DropZone.vue';
import SvgControls from './components/panels/SvgControls.vue';
import WebpControls from './components/panels/WebpControls.vue';
import Previewer from './components/workspace/Previewer.vue';
import { useTheme } from './composables/useTheme';
import { useLocale } from './composables/useLocale';
import { convertToSvg, convertToWebp } from './api/client';
import type { TabMode, SvgParams, WebpParams } from './types';

// Theme & Locale management
const { initTheme } = useTheme();
const { initLocale, t } = useLocale();

// Tab state
const currentTab = ref<TabMode>('svg');

// File state
const currentFile = ref<File | null>(null);
const originalPreviewUrl = ref<string>('');
const originalSize = ref<number>(0);

// Status
const isProcessing = ref<boolean>(false);
const durationMs = ref<number>(0);

// SVG Result
const resultSvg = ref<string>('');
const svgOutputSize = ref<number>(0);

// WebP Result
const resultWebpUri = ref<string>('');
const webpOutputSize = ref<number>(0);

// Parameters
const svgParams = ref<SvgParams>({
  preset: 'icon',
  colormode: 'color',
  hierarchical: 'stacked',
  mode: 'spline',
  color_precision: 6,
  filter_speckle: 4,
  layer_difference: 16,
  corner_threshold: 60,
  length_threshold: 4.0,
  max_iterations: 10,
  splice_threshold: 45,
  path_precision: 3,
});

const webpParams = ref<WebpParams>({
  quality: 80,
  lossless: false,
  method: 6,
  max_width: null,
  max_height: null,
});

const outputSize = computed(() => {
  return currentTab.value === 'svg' ? svgOutputSize.value : webpOutputSize.value;
});

function handleFileSelected(file: File) {
  if (!file) return;
  currentFile.value = file;
  originalSize.value = file.size;
  if (originalPreviewUrl.value) {
    URL.revokeObjectURL(originalPreviewUrl.value);
  }
  originalPreviewUrl.value = URL.createObjectURL(file);
  executeConversion();
}

function handleTabChange(tab: TabMode) {
  currentTab.value = tab;
  if (currentFile.value) {
    executeConversion();
  }
}

let debounceTimer: ReturnType<typeof setTimeout> | null = null;
function triggerAutoConvert() {
  if (!currentFile.value) return;
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    executeConversion();
  }, 250);
}

async function executeConversion() {
  if (!currentFile.value || isProcessing.value) return;

  isProcessing.value = true;
  try {
    if (currentTab.value === 'svg') {
      const res = await convertToSvg(currentFile.value, svgParams.value);
      if (res.success && res.svg_content) {
        resultSvg.value = res.svg_content;
        svgOutputSize.value = res.output_size_bytes || 0;
        durationMs.value = res.duration_ms || 0;
      } else {
        alert(res.error_message || t('common.svgFailed'));
      }
    } else {
      const res = await convertToWebp(currentFile.value, webpParams.value);
      if (res.success && res.webp_data_uri) {
        resultWebpUri.value = res.webp_data_uri;
        webpOutputSize.value = res.output_size_bytes || 0;
        durationMs.value = res.duration_ms || 0;
      } else {
        alert(res.error_message || t('common.webpFailed'));
      }
    }
  } catch (err: any) {
    console.error('Conversion failed:', err);
    alert(t('common.requestFailed'));
  } finally {
    isProcessing.value = false;
  }
}

function resetParams() {
  if (currentTab.value === 'svg') {
    svgParams.value = {
      preset: 'icon',
      colormode: 'color',
      hierarchical: 'stacked',
      mode: 'spline',
      color_precision: 6,
      filter_speckle: 4,
      layer_difference: 16,
      corner_threshold: 60,
      length_threshold: 4.0,
      max_iterations: 10,
      splice_threshold: 45,
      path_precision: 3,
    };
  } else {
    webpParams.value = {
      quality: 80,
      lossless: false,
      method: 6,
      max_width: null,
      max_height: null,
    };
  }
  triggerAutoConvert();
}

function handlePaste(e: ClipboardEvent) {
  const items = e.clipboardData?.items;
  if (!items) return;
  for (let i = 0; i < items.length; i++) {
    if (items[i].type.startsWith('image/')) {
      const file = items[i].getAsFile();
      if (file) {
        handleFileSelected(file);
        break;
      }
    }
  }
}

onMounted(() => {
  initTheme();
  initLocale();
  window.addEventListener('paste', handlePaste);
});

onUnmounted(() => {
  window.removeEventListener('paste', handlePaste);
  if (originalPreviewUrl.value) {
    URL.revokeObjectURL(originalPreviewUrl.value);
  }
});
</script>

<template>
  <div class="flex flex-col min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 transition-colors duration-200">
    <!-- 顶部导航栏 -->
    <Header :current-tab="currentTab" @update:current-tab="handleTabChange" />

    <!-- 主体区域 -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- 左侧控制面板 (5 cols) -->
      <section class="lg:col-span-5 flex flex-col space-y-5">
        <!-- 上传拖拽区 -->
        <DropZone @file-selected="handleFileSelected" />

        <!-- 参数调节卡片 -->
        <div class="bg-white/80 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm dark:shadow-xl space-y-5">
          <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
            <h2 class="text-sm font-bold text-slate-800 dark:text-slate-200 flex items-center space-x-2">
              <span>⚙️</span>
              <span>{{ currentTab === 'svg' ? t('svg.panelTitle') : t('webp.panelTitle') }}</span>
            </h2>
            <button
              @click="resetParams"
              class="text-xs text-slate-500 hover:text-indigo-600 dark:text-slate-400 dark:hover:text-indigo-400 transition-colors cursor-pointer">
              {{ t('common.reset') }}
            </button>
          </div>

          <!-- SVG 参数面板 -->
          <SvgControls
            v-if="currentTab === 'svg'"
            v-model:params="svgParams"
            @change="triggerAutoConvert" />

          <!-- WebP 参数面板 -->
          <WebpControls
            v-else
            v-model:params="webpParams"
            @change="triggerAutoConvert" />

          <!-- 执行转换按钮 -->
          <button
            @click="executeConversion"
            :disabled="!currentFile || isProcessing"
            class="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-sm rounded-xl shadow-lg shadow-indigo-600/30 transition-all flex items-center justify-center space-x-2 cursor-pointer">
            <span v-if="isProcessing" class="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            <span>{{ isProcessing ? t('common.processing') : t('common.execute') }}</span>
          </button>
        </div>
      </section>

      <!-- 右侧对比与展示面板 (7 cols) -->
      <section class="lg:col-span-7 flex flex-col space-y-5">
        <Previewer
          :current-tab="currentTab"
          :current-file="currentFile"
          :original-preview-url="originalPreviewUrl"
          :original-size="originalSize"
          :output-size="outputSize"
          :duration-ms="durationMs"
          :is-processing="isProcessing"
          :result-svg="resultSvg"
          :result-webp-uri="resultWebpUri" />
      </section>
    </main>
  </div>
</template>
