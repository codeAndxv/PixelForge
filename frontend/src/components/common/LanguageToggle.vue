<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { Languages, Check } from 'lucide-vue-next';
import { useLocale } from '../../composables/useLocale';
import type { LocaleCode } from '../../locales/types';

const { locale, setLocale, availableLocales, currentOption, t } = useLocale();

const isOpen = ref(false);
const dropdownRef = ref<HTMLDivElement | null>(null);

function toggleDropdown() {
  isOpen.value = !isOpen.value;
}

function selectLocale(code: LocaleCode) {
  setLocale(code);
  isOpen.value = false;
}

function handleClickOutside(event: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  window.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div ref="dropdownRef" class="relative inline-block text-left">
    <button
      @click.stop="toggleDropdown"
      type="button"
      :title="t('language.selectLanguage')"
      class="p-2 rounded-xl text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100 bg-slate-100 dark:bg-slate-800/80 hover:bg-slate-200 dark:hover:bg-slate-700/80 border border-slate-200 dark:border-slate-700/60 shadow-sm transition-all duration-200 cursor-pointer flex items-center space-x-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 text-xs font-semibold">
      <Languages class="w-4 h-4 text-indigo-500 dark:text-indigo-400" />
      <span class="hidden sm:inline">{{ currentOption.shortLabel }}</span>
    </button>

    <!-- 下拉菜单 -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-36 origin-top-right rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl z-50 py-1.5 focus:outline-none backdrop-blur-md">
      <button
        v-for="item in availableLocales"
        :key="item.code"
        @click="selectLocale(item.code)"
        :class="locale === item.code ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 font-bold' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'"
        class="w-full text-left px-3.5 py-2 text-xs flex items-center justify-between transition-colors cursor-pointer">
        <span class="flex items-center space-x-2">
          <span>{{ item.flag }}</span>
          <span>{{ item.label }}</span>
        </span>
        <Check v-if="locale === item.code" class="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
      </button>
    </div>
  </div>
</template>
