"""
Core conversion logic for VTracer image-to-SVG.
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import vtracer

from .presets import PRESETS, PresetType


class ConversionResult:
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        duration_ms: float,
        input_size_bytes: int,
        output_size_bytes: int,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.duration_ms = duration_ms
        self.input_size_bytes = input_size_bytes
        self.output_size_bytes = output_size_bytes
        self.success = success
        self.error_message = error_message

    @property
    def size_change_ratio(self) -> float:
        if self.input_size_bytes == 0:
            return 0.0
        return self.output_size_bytes / self.input_size_bytes


def convert_image(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    preset: PresetType = PresetType.ICON,
    custom_params: Optional[Dict[str, Any]] = None,
) -> ConversionResult:
    """
    Convert a single image (PNG/JPEG/etc.) to SVG.

    :param input_path: Path to the input image.
    :param output_path: Destination SVG path. If None, uses input file name with .svg.
    :param preset: Image style preset (ICON, ILLUSTRATION, PHOTO, LINEART, PIXELART).
    :param custom_params: Override specific VTracer parameters.
    """
    input_p = Path(input_path).resolve()
    if not input_p.exists():
        raise FileNotFoundError(f"Input image not found: {input_p}")

    if output_path is None:
        output_p = input_p.with_suffix(".svg")
    else:
        output_p = Path(output_path).resolve()

    output_p.parent.mkdir(parents=True, exist_ok=True)

    # Base parameters from preset
    params = dict(PRESETS.get(preset, PRESETS[PresetType.ICON]))

    # Apply overrides
    if custom_params:
        params.update({k: v for k, v in custom_params.items() if v is not None})

    input_size = input_p.stat().st_size
    start_time = time.perf_counter()

    try:
        vtracer.convert_image_to_svg_py(
            str(input_p),
            str(output_p),
            colormode=params.get("colormode"),
            hierarchical=params.get("hierarchical"),
            mode=params.get("mode"),
            filter_speckle=params.get("filter_speckle"),
            color_precision=params.get("color_precision"),
            layer_difference=params.get("layer_difference"),
            corner_threshold=params.get("corner_threshold"),
            length_threshold=params.get("length_threshold"),
            max_iterations=params.get("max_iterations"),
            splice_threshold=params.get("splice_threshold"),
            path_precision=params.get("path_precision"),
        )
        duration_ms = (time.perf_counter() - start_time) * 1000
        output_size = output_p.stat().st_size if output_p.exists() else 0

        return ConversionResult(
            input_path=input_p,
            output_path=output_p,
            duration_ms=duration_ms,
            input_size_bytes=input_size,
            output_size_bytes=output_size,
            success=True,
        )
    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        return ConversionResult(
            input_path=input_p,
            output_path=output_p,
            duration_ms=duration_ms,
            input_size_bytes=input_size,
            output_size_bytes=0,
            success=False,
            error_message=str(e),
        )


class BytesConversionResult:
    def __init__(
        self,
        svg_content: str,
        input_size_bytes: int,
        output_size_bytes: int,
        duration_ms: float,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        self.svg_content = svg_content
        self.input_size_bytes = input_size_bytes
        self.output_size_bytes = output_size_bytes
        self.duration_ms = duration_ms
        self.success = success
        self.error_message = error_message


def convert_bytes_to_svg(
    image_bytes: bytes,
    image_format: str = "png",
    preset: PresetType = PresetType.ICON,
    custom_params: Optional[Dict[str, Any]] = None,
) -> BytesConversionResult:
    """
    Convert in-memory image bytes to SVG string.
    """
    input_size = len(image_bytes)
    start_time = time.perf_counter()

    params = dict(PRESETS.get(preset, PRESETS[PresetType.ICON]))
    if custom_params:
        params.update({k: v for k, v in custom_params.items() if v is not None})

    try:
        svg_str = vtracer.convert_raw_image_to_svg(
            image_bytes,
            img_format=image_format.lower().replace("jpeg", "jpg"),
            colormode=params.get("colormode"),
            hierarchical=params.get("hierarchical"),
            mode=params.get("mode"),
            filter_speckle=params.get("filter_speckle"),
            color_precision=params.get("color_precision"),
            layer_difference=params.get("layer_difference"),
            corner_threshold=params.get("corner_threshold"),
            length_threshold=params.get("length_threshold"),
            max_iterations=params.get("max_iterations"),
            splice_threshold=params.get("splice_threshold"),
            path_precision=params.get("path_precision"),
        )
        duration_ms = (time.perf_counter() - start_time) * 1000
        output_size = len(svg_str.encode("utf-8"))

        return BytesConversionResult(
            svg_content=svg_str,
            input_size_bytes=input_size,
            output_size_bytes=output_size,
            duration_ms=duration_ms,
            success=True,
        )
    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        return BytesConversionResult(
            svg_content="",
            input_size_bytes=input_size,
            output_size_bytes=0,
            duration_ms=duration_ms,
            success=False,
            error_message=str(e),
        )


def batch_convert(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    preset: PresetType = PresetType.ICON,
    patterns: Tuple[str, ...] = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp"),
    custom_params: Optional[Dict[str, Any]] = None,
) -> List[ConversionResult]:
    """
    Batch convert multiple images in a directory.
    """
    in_dir = Path(input_dir).resolve()
    if not in_dir.is_dir():
        raise NotADirectoryError(f"Directory not found: {in_dir}")

    out_dir = Path(output_dir).resolve() if output_dir else in_dir / "svg_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    image_files: List[Path] = []
    for pattern in patterns:
        image_files.extend(in_dir.glob(pattern))

    results: List[ConversionResult] = []
    for img_path in sorted(image_files):
        target_svg = out_dir / f"{img_path.stem}.svg"
        res = convert_image(
            input_path=img_path,
            output_path=target_svg,
            preset=preset,
            custom_params=custom_params,
        )
        results.append(res)

    return results

