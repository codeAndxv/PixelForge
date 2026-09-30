"""
WebP conversion engine using Pillow.
"""

import io
import time
from pathlib import Path
from typing import List, Optional, Tuple, Union
from PIL import Image


class WebPResult:
    def __init__(
        self,
        input_size_bytes: int,
        output_size_bytes: int,
        duration_ms: float,
        original_width: int,
        original_height: int,
        output_width: int,
        output_height: int,
        output_bytes: Optional[bytes] = None,
        output_path: Optional[Path] = None,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        self.input_size_bytes = input_size_bytes
        self.output_size_bytes = output_size_bytes
        self.duration_ms = duration_ms
        self.original_width = original_width
        self.original_height = original_height
        self.output_width = output_width
        self.output_height = output_height
        self.output_bytes = output_bytes
        self.output_path = output_path
        self.success = success
        self.error_message = error_message

    @property
    def reduction_percentage(self) -> float:
        """Percentage of file size reduced (e.g. 75.4 means 75.4% smaller)."""
        if self.input_size_bytes == 0:
            return 0.0
        return max(0.0, (1.0 - (self.output_size_bytes / self.input_size_bytes)) * 100.0)


def convert_bytes_to_webp(
    image_bytes: bytes,
    quality: int = 80,
    lossless: bool = False,
    method: int = 6,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
) -> WebPResult:
    """
    Convert in-memory image bytes to WebP bytes.
    """
    input_size = len(image_bytes)
    start_time = time.perf_counter()

    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            orig_w, orig_h = img.size
            out_w, out_h = orig_w, orig_h

            # Scale if max dimension limits provided
            if (max_width and orig_w > max_width) or (max_height and orig_h > max_height):
                ratio_w = max_width / orig_w if max_width else 1.0
                ratio_h = max_height / orig_h if max_height else 1.0
                ratio = min(ratio_w, ratio_h)
                out_w = max(1, int(orig_w * ratio))
                out_h = max(1, int(orig_h * ratio))
                img = img.resize((out_w, out_h), Image.Resampling.LANCZOS)

            # Ensure RGBA / RGB mode compatibility
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA" if "transparency" in img.info or img.mode == "LA" else "RGB")

            out_buffer = io.BytesIO()
            img.save(
                out_buffer,
                format="WEBP",
                quality=max(1, min(100, quality)),
                lossless=lossless,
                method=max(0, min(6, method)),
            )

            webp_bytes = out_buffer.getvalue()
            duration_ms = (time.perf_counter() - start_time) * 1000

            return WebPResult(
                input_size_bytes=input_size,
                output_size_bytes=len(webp_bytes),
                duration_ms=duration_ms,
                original_width=orig_w,
                original_height=orig_h,
                output_width=out_w,
                output_height=out_h,
                output_bytes=webp_bytes,
                success=True,
            )
    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        return WebPResult(
            input_size_bytes=input_size,
            output_size_bytes=0,
            duration_ms=duration_ms,
            original_width=0,
            original_height=0,
            output_width=0,
            output_height=0,
            success=False,
            error_message=str(e),
        )


def convert_image_to_webp(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    quality: int = 80,
    lossless: bool = False,
    method: int = 6,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
) -> WebPResult:
    """
    Convert a file from disk to a WebP file on disk.
    """
    input_p = Path(input_path).resolve()
    if not input_p.exists():
        raise FileNotFoundError(f"Image not found: {input_p}")

    if output_path is None:
        output_p = input_p.with_suffix(".webp")
    else:
        output_p = Path(output_path).resolve()

    output_p.parent.mkdir(parents=True, exist_ok=True)

    with open(input_p, "rb") as f:
        img_bytes = f.read()

    result = convert_bytes_to_webp(
        image_bytes=img_bytes,
        quality=quality,
        lossless=lossless,
        method=method,
        max_width=max_width,
        max_height=max_height,
    )

    if result.success and result.output_bytes:
        with open(output_p, "wb") as f:
            f.write(result.output_bytes)
        result.output_path = output_p

    return result


def batch_convert_webp(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    quality: int = 80,
    lossless: bool = False,
    patterns: Tuple[str, ...] = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tiff"),
) -> List[WebPResult]:
    """
    Batch convert images in a directory to WebP.
    """
    in_dir = Path(input_dir).resolve()
    if not in_dir.is_dir():
        raise NotADirectoryError(f"Directory not found: {in_dir}")

    out_dir = Path(output_dir).resolve() if output_dir else in_dir / "webp_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    image_files: List[Path] = []
    for pattern in patterns:
        image_files.extend(in_dir.glob(pattern))

    results: List[WebPResult] = []
    for img_path in sorted(image_files):
        target_webp = out_dir / f"{img_path.stem}.webp"
        res = convert_image_to_webp(
            input_path=img_path,
            output_path=target_webp,
            quality=quality,
            lossless=lossless,
        )
        results.append(res)

    return results
