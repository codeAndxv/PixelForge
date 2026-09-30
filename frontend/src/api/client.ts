import type { PresetsMap, SvgConvertResponse, SvgParams, WebpConvertResponse, WebpParams } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export async function fetchPresets(): Promise<PresetsMap> {
  const res = await fetch(`${API_BASE}/presets`);
  if (!res.ok) {
    throw new Error(`Failed to fetch presets: ${res.statusText}`);
  }
  return res.json();
}

export async function convertToSvg(file: File, params: SvgParams): Promise<SvgConvertResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('preset', params.preset);
  formData.append('colormode', params.colormode);
  formData.append('hierarchical', params.hierarchical);
  formData.append('mode', params.mode);
  formData.append('filter_speckle', String(params.filter_speckle));
  formData.append('color_precision', String(params.color_precision));
  formData.append('layer_difference', String(params.layer_difference));
  formData.append('corner_threshold', String(params.corner_threshold));
  formData.append('length_threshold', String(params.length_threshold));
  formData.append('max_iterations', String(params.max_iterations));
  formData.append('splice_threshold', String(params.splice_threshold));
  formData.append('path_precision', String(params.path_precision));

  const res = await fetch(`${API_BASE}/convert/svg`, {
    method: 'POST',
    body: formData,
  });

  return res.json();
}

export async function convertToWebp(file: File, params: WebpParams): Promise<WebpConvertResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('quality', String(params.quality));
  formData.append('lossless', String(params.lossless));
  formData.append('method', String(params.method));
  if (params.max_width) {
    formData.append('max_width', String(params.max_width));
  }
  if (params.max_height) {
    formData.append('max_height', String(params.max_height));
  }

  const res = await fetch(`${API_BASE}/convert/webp`, {
    method: 'POST',
    body: formData,
  });

  return res.json();
}
