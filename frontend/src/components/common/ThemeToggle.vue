<script setup lang="ts">
import { Sun, Moon } from 'lucide-vue-next';
import { useTheme } from '../../composables/useTheme';
import { useLocale } from '../../composables/useLocale';

const { isDark, toggleTheme } = useTheme();
const { t } = useLocale();
</script>

<template>
  <button
    @click="toggleTheme"
    type="button"
    :title="isDark ? t('theme.toLight') : t('theme.toDark')"
    class="relative p-2 rounded-xl text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100 bg-slate-100 dark:bg-slate-800/80 hover:bg-slate-200 dark:hover:bg-slate-700/80 border border-slate-200 dark:border-slate-700/60 shadow-sm transition-all duration-200 cursor-pointer flex items-center justify-center group focus:outline-none focus:ring-2 focus:ring-indigo-500/50">
    <!-- 浅色模式下显示太阳图标 -->
    <Sun
      v-if="!isDark"
      class="w-4 h-4 text-amber-500 transition-transform duration-300 transform rotate-0 group-hover:rotate-45" />

    <!-- 深色模式下显示月亮图标 -->
    <Moon
      v-else
      class="w-4 h-4 text-indigo-400 transition-transform duration-300 transform rotate-0 group-hover:-rotate-12" />
  </button>
</template>
