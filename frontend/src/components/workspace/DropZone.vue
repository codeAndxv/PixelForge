<script setup lang="ts">
import { ref } from 'vue';
import { useLocale } from '../../composables/useLocale';

const emit = defineEmits<{
  (e: 'file-selected', file: File): void;
}>();

const { t } = useLocale();
const isDragging = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

function handleFileSelect(e: Event) {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    emit('file-selected', target.files[0]);
    target.value = ''; // Reset for re-selecting same file
  }
}

function handleDrop(e: DragEvent) {
  isDragging.value = false;
  if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    emit('file-selected', e.dataTransfer.files[0]);
  }
}

function triggerClick() {
  fileInput.value?.click();
}
</script>

<template>
  <div
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
    @click="triggerClick"
    :class="isDragging ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-500/10 shadow-indigo-500/10' : 'border-slate-300 hover:border-slate-400 dark:border-slate-800 dark:hover:border-slate-700 bg-white/70 dark:bg-slate-900/60 shadow-xs dark:shadow-xl'"
    class="relative border-2 border-dashed rounded-2xl p-6 text-center transition-all cursor-pointer group">
    <input
      type="file"
      ref="fileInput"
      @change="handleFileSelect"
      accept="image/png, image/jpeg, image/webp, image/bmp"
      class="hidden" />

    <div class="space-y-2">
      <div class="w-12 h-12 mx-auto rounded-2xl bg-slate-100 dark:bg-slate-800 group-hover:bg-indigo-50 dark:group-hover:bg-indigo-600/20 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 text-slate-500 dark:text-slate-400 flex items-center justify-center text-2xl transition-all shadow-inner">
        📥
      </div>
      <div class="text-sm font-semibold text-slate-800 dark:text-slate-200">
        {{ t('dropzone.dragHint') }} <span class="text-indigo-600 dark:text-indigo-400 underline underline-offset-4 font-bold">{{ t('dropzone.clickUpload') }}</span>
      </div>
      <p class="text-xs text-slate-500 dark:text-slate-400">
        {{ t('dropzone.supportedFormats') }}（<kbd class="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded border border-slate-300 dark:border-slate-700 text-[10px] text-slate-700 dark:text-slate-300 font-mono">{{ t('dropzone.pasteHint') }}</kbd>）
      </p>
    </div>
  </div>
</template>
