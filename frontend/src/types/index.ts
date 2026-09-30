export type TabMode = 'svg' | 'webp';

export type SvgPreset = 'icon' | 'illustration' | 'photo' | 'lineart' | 'pixelart';

export interface SvgParams {
  preset: SvgPreset;
  colormode: 'color' | 'binary';
  hierarchical: 'stacked' | 'cutout';
  mode: 'spline' | 'polygon' | 'none';
  filter_speckle: number;
  color_precision: number;
  layer_difference: number;
  corner_threshold: number;
  length_threshold: number;
  max_iterations: number;
  splice_threshold: number;
  path_precision: number;
}

export interface WebpParams {
  quality: number;
  lossless: boolean;
  method: number;
  max_width: number | null;
  max_height: number | null;
}

export interface SvgConvertResponse {
  success: boolean;
  svg_content?: string;
  input_size_bytes?: number;
  output_size_bytes?: number;
  duration_ms?: number;
  error_message?: string;
}

export interface WebpConvertResponse {
  success: boolean;
  webp_data_uri?: string;
  input_size_bytes?: number;
  output_size_bytes?: number;
  reduction_percentage?: number;
  original_width?: number;
  original_height?: number;
  output_width?: number;
  output_height?: number;
  duration_ms?: number;
  error_message?: string;
}

export interface PresetsMap {
  [key: string]: Partial<SvgParams>;
}
