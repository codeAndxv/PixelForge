import { zhCN } from './zh-CN';
import { enUS } from './en-US';
import type { LocaleCode, LocaleMessage, LocaleOption } from './types';

export * from './types';

export const messages: Record<LocaleCode, LocaleMessage> = {
  'zh-CN': zhCN,
  'en-US': enUS,
};

export const AVAILABLE_LOCALES: LocaleOption[] = [
  {
    code: 'zh-CN',
    label: '简体中文',
    shortLabel: '中文',
    flag: '🇨🇳',
  },
  {
    code: 'en-US',
    label: 'English',
    shortLabel: 'EN',
    flag: '🇺🇸',
  },
];
