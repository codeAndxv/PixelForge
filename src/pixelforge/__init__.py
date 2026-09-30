from .converter import convert_image, convert_bytes_to_svg, batch_convert, PresetType
from .webp_converter import convert_image_to_webp, convert_bytes_to_webp, batch_convert_webp, WebPResult
from .presets import PRESETS

__version__ = "0.1.0"
__all__ = [
    "convert_image",
    "convert_bytes_to_svg",
    "batch_convert",
    "convert_image_to_webp",
    "convert_bytes_to_webp",
    "batch_convert_webp",
    "WebPResult",
    "PresetType",
    "PRESETS",
]

