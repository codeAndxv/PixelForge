<script setup lang="ts">
import { computed } from 'vue';
import type { SvgParams, SvgPreset } from '../../types';
import { useLocale } from '../../composables/useLocale';

const props = defineProps<{
  params: SvgParams;
}>();

const emit = defineEmits<{
  (e: 'update:params', params: SvgParams): void;
  (e: 'change'): void;
}>();

const { t } = useLocale();

const presetsKeys: SvgPreset[] = ['icon', 'illustration', 'photo', 'lineart', 'pixelart'];

const presetsList = computed(() => {
  return presetsKeys.map((key) => ({
    key,
    label: t(`presets.${key}`),
  }));
});

function applyPreset(presetKey: SvgPreset) {
  const updated: SvgParams = { ...props.params, preset: presetKey };
  if (presetKey === 'icon') {
    updated.color_precision = 6;
    updated.filter_speckle = 4;
    updated.path_precision = 3;
    updated.colormode = 'color';
    updated.hierarchical = 'stacked';
  } else if (presetKey === 'illustration') {
    updated.color_precision = 7;
    updated.filter_speckle = 6;
    updated.path_precision = 4;
    updated.colormode = 'color';
    updated.hierarchical = 'stacked';
  } else if (presetKey === 'photo') {
    updated.color_precision = 8;
    updated.filter_speckle = 10;
    updated.path_precision = 5;
    updated.colormode = 'color';
    updated.hierarchical = 'stacked';
  } else if (presetKey === 'lineart') {
    updated.color_precision = 4;
    updated.filter_speckle = 4;
    updated.path_precision = 3;
    updated.colormode = 'binary';
    updated.hierarchical = 'cutout';
  } else if (presetKey === 'pixelart') {
    updated.color_precision = 8;
    updated.filter_speckle = 0;
    updated.path_precision = 2;
    updated.colormode = 'color';
    updated.hierarchical = 'stacked';
  }
  emit('update:params', updated);
  emit('change');
}

function updateField<K extends keyof SvgParams>(key: K, value: SvgParams[K]) {
  const updated = { ...props.params, [key]: value };
  emit('update:params', updated);
  emit('change');
}
</script>

<template>
  <div class="space-y-4 text-xs">
    <!-- 预设选择 -->
    <div>
      <label class="block text-slate-600 dark:text-slate-400 mb-1.5 font-medium">{{ t('svg.presetLabel') }}</label>
      <div class="grid grid-cols-3 gap-2">
        <button
          v-for="p in presetsList"
          :key="p.key"
          @click="applyPreset(p.key)"
          :class="params.preset === p.key ? 'bg-indigo-600 text-white font-bold shadow-md shadow-indigo-600/30' : 'bg-slate-100 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700/80 border border-slate-200 dark:border-transparent'"
          class="py-1.5 px-2 rounded-lg text-center transition-all cursor-pointer">
          {{ p.label }}
        </button>
      </div>
    </div>

    <!-- 色彩精度 -->
    <div class="space-y-1">
      <div class="flex justify-between text-slate-600 dark:text-slate-400">
        <span>{{ t('svg.colorPrecision') }}</span>
        <span class="text-indigo-600 dark:text-indigo-400 font-mono font-bold">{{ params.color_precision }}</span>
      </div>
      <input
        type="range"
        min="1"
        max="8"
        step="1"
        :value="params.color_precision"
        @input="(e) => updateField('color_precision', Number((e.target as HTMLInputElement).value))"
        class="w-full accent-indigo-600 h-1.5 bg-slate-200 dark:bg-slate-800 rounded-lg cursor-pointer" />
      <div class="flex justify-between text-[10px] text-slate-400 dark:text-slate-500">
        <span>{{ t('svg.colorPrecisionMin') }}</span>
        <span>{{ t('svg.colorPrecisionMax') }}</span>
      </div>
    </div>

    <!-- 噪点过滤 -->
    <div class="space-y-1">
      <div class="flex justify-between text-slate-600 dark:text-slate-400">
        <span>{{ t('svg.filterSpeckle') }}</span>
        <span class="text-indigo-600 dark:text-indigo-400 font-mono font-bold">{{ params.filter_speckle }} px</span>
      </div>
      <input
        type="range"
        min="0"
        max="40"
        step="2"
        :value="params.filter_speckle"
        @input="(e) => updateField('filter_speckle', Number((e.target as HTMLInputElement).value))"
        class="w-full accent-indigo-600 h-1.5 bg-slate-200 dark:bg-slate-800 rounded-lg cursor-pointer" />
      <div class="flex justify-between text-[10px] text-slate-400 dark:text-slate-500">
        <span>{{ t('svg.filterSpeckleMin') }}</span>
        <span>{{ t('svg.filterSpeckleMax') }}</span>
      </div>
    </div>

    <!-- 坐标小数精度 -->
    <div class="space-y-1">
      <div class="flex justify-between text-slate-600 dark:text-slate-400">
        <span>{{ t('svg.pathPrecision') }}</span>
        <span class="text-indigo-600 dark:text-indigo-400 font-mono font-bold">{{ params.path_precision }} {{ t('svg.pathPrecisionUnit') }}</span>
      </div>
      <input
        type="range"
        min="1"
        max="5"
        step="1"
        :value="params.path_precision"
        @input="(e) => updateField('path_precision', Number((e.target as HTMLInputElement).value))"
        class="w-full accent-indigo-600 h-1.5 bg-slate-200 dark:bg-slate-800 rounded-lg cursor-pointer" />
    </div>

    <!-- 曲线与图层选项 -->
    <div class="grid grid-cols-2 gap-3 pt-1">
      <div>
        <label class="block text-slate-600 dark:text-slate-400 mb-1">{{ t('svg.colorMode') }}</label>
        <select
          :value="params.colormode"
          @change="(e) => updateField('colormode', (e.target as HTMLSelectElement).value as any)"
          class="w-full bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 cursor-pointer">
          <option value="color">{{ t('svg.colorModeColor') }}</option>
          <option value="binary">{{ t('svg.colorModeBinary') }}</option>
        </select>
      </div>
      <div>
        <label class="block text-slate-600 dark:text-slate-400 mb-1">{{ t('svg.hierarchical') }}</label>
        <select
          :value="params.hierarchical"
          @change="(e) => updateField('hierarchical', (e.target as HTMLSelectElement).value as any)"
          class="w-full bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 cursor-pointer">
          <option value="stacked">{{ t('svg.hierarchicalStacked') }}</option>
          <option value="cutout">{{ t('svg.hierarchicalCutout') }}</option>
        </select>
      </div>
    </div>
  </div>
</template>
