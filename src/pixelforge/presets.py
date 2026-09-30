"""
Presets for various image types for VTracer vectorization.
"""

from typing import Any, Dict
from enum import Enum


class PresetType(str, Enum):
    ICON = "icon"
    ILLUSTRATION = "illustration"
    PHOTO = "photo"
    LINEART = "lineart"
    PIXELART = "pixelart"
    CUSTOM = "custom"


# Detailed parameter settings for each preset
PRESETS: Dict[PresetType, Dict[str, Any]] = {
    # 适合扁平图标、Logo、单色/简单色块矢量图形
    PresetType.ICON: {
        "colormode": "color",
        "hierarchical": "stacked",
        "mode": "spline",
        "filter_speckle": 4,
        "color_precision": 6,
        "layer_difference": 16,
        "corner_threshold": 60,
        "length_threshold": 4.0,
        "max_iterations": 10,
        "splice_threshold": 45,
        "path_precision": 3,
    },
    # 适合动漫插画、手绘插图、卡通风格多色图
    PresetType.ILLUSTRATION: {
        "colormode": "color",
        "hierarchical": "stacked",
        "mode": "spline",
        "filter_speckle": 6,
        "color_precision": 7,
        "layer_difference": 12,
        "corner_threshold": 50,
        "length_threshold": 3.5,
        "max_iterations": 10,
        "splice_threshold": 45,
        "path_precision": 4,
    },
    # 适合写实照片、复杂渐变图形（更精细的色阶与噪点过滤）
    PresetType.PHOTO: {
        "colormode": "color",
        "hierarchical": "stacked",
        "mode": "spline",
        "filter_speckle": 10,
        "color_precision": 8,
        "layer_difference": 8,
        "corner_threshold": 40,
        "length_threshold": 2.5,
        "max_iterations": 10,
        "splice_threshold": 45,
        "path_precision": 5,
    },
    # 适合黑白线稿、签名、单色简笔画
    PresetType.LINEART: {
        "colormode": "binary",
        "hierarchical": "stacked",
        "mode": "spline",
        "filter_speckle": 4,
        "color_precision": 4,
        "layer_difference": 16,
        "corner_threshold": 60,
        "length_threshold": 4.0,
        "max_iterations": 10,
        "splice_threshold": 45,
        "path_precision": 3,
    },
    # 适合像素游戏图、像素风图标（硬边多边形拟合）
    PresetType.PIXELART: {
        "colormode": "color",
        "hierarchical": "stacked",
        "mode": "polygon",
        "filter_speckle": 0,
        "color_precision": 8,
        "layer_difference": 0,
        "corner_threshold": 180,
        "length_threshold": 0.0,
        "max_iterations": 1,
        "splice_threshold": 0,
        "path_precision": 2,
    },
}
