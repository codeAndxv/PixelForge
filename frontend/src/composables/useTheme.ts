import { ref, computed } from 'vue';

export type ThemeMode = 'light' | 'dark';

const THEME_KEY = 'pixelforge-theme';

// Shared state across all component instances
const currentTheme = ref<ThemeMode>('dark');

export function useTheme() {
  function initTheme() {
    const saved = localStorage.getItem(THEME_KEY) as ThemeMode | null;
    if (saved && (saved === 'light' || saved === 'dark')) {
      setTheme(saved);
    } else {
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      setTheme(prefersDark ? 'dark' : 'dark'); // Default to dark for premium studio feel, or prefersDark
    }
  }

  function setTheme(theme: ThemeMode) {
    currentTheme.value = theme;
    localStorage.setItem(THEME_KEY, theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  function toggleTheme() {
    setTheme(currentTheme.value === 'dark' ? 'light' : 'dark');
  }

  const isDark = computed(() => currentTheme.value === 'dark');

  return {
    theme: currentTheme,
    isDark,
    initTheme,
    setTheme,
    toggleTheme,
  };
}
