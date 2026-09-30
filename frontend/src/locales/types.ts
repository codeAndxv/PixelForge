export interface LocaleMessage {
  common: {
    reset: string;
    execute: string;
    processing: string;
    copy: string;
    copied: string;
    download: string;
    downloadSvg: string;
    downloadWebp: string;
    duration: string;
    requestFailed: string;
    svgFailed: string;
    webpFailed: string;
  };
  header: {
    title: string;
    subtitle: string;
    tabSvg: string;
    tabWebp: string;
    apiActive: string;
  };
  theme: {
    toLight: string;
    toDark: string;
  };
  language: {
    selectLanguage: string;
    zhCN: string;
    enUS: string;
  };
  dropzone: {
    dragHint: string;
    clickUpload: string;
    supportedFormats: string;
    pasteHint: string;
  };
  presets: {
    icon: string;
    iconDesc: string;
    illustration: string;
    illustrationDesc: string;
    photo: string;
    photoDesc: string;
    lineart: string;
    lineartDesc: string;
    pixelart: string;
    pixelartDesc: string;
  };
  svg: {
    panelTitle: string;
    presetLabel: string;
    colorPrecision: string;
    colorPrecisionMin: string;
    colorPrecisionMax: string;
    filterSpeckle: string;
    filterSpeckleMin: string;
    filterSpeckleMax: string;
    pathPrecision: string;
    pathPrecisionUnit: string;
    colorMode: string;
    colorModeColor: string;
    colorModeBinary: string;
    hierarchical: string;
    hierarchicalStacked: string;
    hierarchicalCutout: string;
  };
  webp: {
    panelTitle: string;
    lossless: string;
    losslessDesc: string;
    quality: string;
    qualityMin: string;
    qualityRec: string;
    qualityMax: string;
    maxWidth: string;
    maxWidthPlaceholder: string;
    maxHeight: string;
    maxHeightPlaceholder: string;
  };
  preview: {
    waitingTitle: string;
    waitingDesc: string;
    originalTitle: string;
    resultSvgTitle: string;
    resultWebpTitle: string;
    sizeReduced: string;
    sizeIncreased: string;
    converting: string;
    clickToConvert: string;
  };
}

export type LocaleCode = 'zh-CN' | 'en-US';

export interface LocaleOption {
  code: LocaleCode;
  label: string;
  shortLabel: string;
  flag: string;
}
