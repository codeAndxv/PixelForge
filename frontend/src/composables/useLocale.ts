import { ref, computed } from 'vue';
import { messages, AVAILABLE_LOCALES } from '../locales';
import type { LocaleCode, LocaleOption } from '../locales/types';

const LOCALE_KEY = 'pixelforge-locale';

// Shared state
const currentLocale = ref<LocaleCode>('zh-CN');

export function useLocale() {
  function initLocale() {
    const saved = localStorage.getItem(LOCALE_KEY) as LocaleCode | null;
    if (saved && (saved === 'zh-CN' || saved === 'en-US')) {
      setLocale(saved);
      return;
    }

    // Detect browser language
    const navLang = navigator.language || (navigator as any).userLanguage || '';
    if (navLang.toLowerCase().startsWith('zh')) {
      setLocale('zh-CN');
    } else {
      setLocale('en-US');
    }
  }

  function setLocale(code: LocaleCode) {
    if (!messages[code]) return;
    currentLocale.value = code;
    localStorage.setItem(LOCALE_KEY, code);
    document.documentElement.lang = code === 'zh-CN' ? 'zh-CN' : 'en';
  }

  /**
   * Translate a key path (e.g. 'header.title', 'presets.icon', 'common.execute')
   */
  function t(path: string): string {
    const keys = path.split('.');
    let current: any = messages[currentLocale.value];

    for (const k of keys) {
      if (current && typeof current === 'object' && k in current) {
        current = current[k];
      } else {
        // Fallback to zh-CN or en-US if key is missing
        let fallback: any = messages['zh-CN'];
        for (const fk of keys) {
          if (fallback && typeof fallback === 'object' && fk in fallback) {
            fallback = fallback[fk];
          } else {
            return path;
          }
        }
        return typeof fallback === 'string' ? fallback : path;
      }
    }

    return typeof current === 'string' ? current : path;
  }

  const currentOption = computed<LocaleOption>(() => {
    return AVAILABLE_LOCALES.find((l) => l.code === currentLocale.value) || AVAILABLE_LOCALES[0];
  });

  return {
    locale: currentLocale,
    t,
    setLocale,
    initLocale,
    availableLocales: AVAILABLE_LOCALES,
    currentOption,
  };
}
