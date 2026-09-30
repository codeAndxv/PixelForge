"""
FastAPI server providing endpoints and static UI for PixelForge.
"""

import base64
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .converter import convert_bytes_to_svg
from .webp_converter import convert_bytes_to_webp
from .presets import PRESETS, PresetType

app = FastAPI(title="PixelForge API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
ASSETS_DIR = STATIC_DIR / "assets"
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "PixelForge API"}


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>PixelForge UI not found</h1>", status_code=404)


@app.get("/api/presets")
async def get_presets():
    return JSONResponse(content={k.value: v for k, v in PRESETS.items()})


@app.post("/api/convert/svg")
async def api_convert_svg(
    file: UploadFile = File(...),
    preset: str = Form("icon"),
    colormode: Optional[str] = Form(None),
    hierarchical: Optional[str] = Form(None),
    filter_speckle: Optional[int] = Form(None),
    color_precision: Optional[int] = Form(None),
    layer_difference: Optional[int] = Form(None),
    corner_threshold: Optional[int] = Form(None),
    length_threshold: Optional[float] = Form(None),
    path_precision: Optional[int] = Form(None),
):
    try:
        content = await file.read()
        filename = file.filename or "image.png"
        fmt = filename.split(".")[-1].lower() if "." in filename else "png"

        # Determine preset
        try:
            p_enum = PresetType(preset)
        except ValueError:
            p_enum = PresetType.ICON

        custom_params = {
            "colormode": colormode,
            "hierarchical": hierarchical,
            "filter_speckle": filter_speckle,
            "color_precision": color_precision,
            "layer_difference": layer_difference,
            "corner_threshold": corner_threshold,
            "length_threshold": length_threshold,
            "path_precision": path_precision,
        }

        res = convert_bytes_to_svg(
            image_bytes=content,
            image_format=fmt,
            preset=p_enum,
            custom_params=custom_params,
        )

        if not res.success:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error_message": res.error_message},
            )

        return JSONResponse(
            content={
                "success": True,
                "svg_content": res.svg_content,
                "input_size_bytes": res.input_size_bytes,
                "output_size_bytes": res.output_size_bytes,
                "duration_ms": round(res.duration_ms, 2),
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error_message": str(e)})


@app.post("/api/convert/webp")
async def api_convert_webp(
    file: UploadFile = File(...),
    quality: int = Form(80),
    lossless: bool = Form(False),
    method: int = Form(6),
    max_width: Optional[int] = Form(None),
    max_height: Optional[int] = Form(None),
):
    try:
        content = await file.read()
        res = convert_bytes_to_webp(
            image_bytes=content,
            quality=quality,
            lossless=lossless,
            method=method,
            max_width=max_width if max_width and max_width > 0 else None,
            max_height=max_height if max_height and max_height > 0 else None,
        )

        if not res.success or not res.output_bytes:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error_message": res.error_message},
            )

        webp_b64 = base64.b64encode(res.output_bytes).decode("utf-8")
        data_uri = f"data:image/webp;base64,{webp_b64}"

        return JSONResponse(
            content={
                "success": True,
                "webp_data_uri": data_uri,
                "input_size_bytes": res.input_size_bytes,
                "output_size_bytes": res.output_size_bytes,
                "reduction_percentage": round(res.reduction_percentage, 1),
                "original_width": res.original_width,
                "original_height": res.original_height,
                "output_width": res.output_width,
                "output_height": res.output_height,
                "duration_ms": round(res.duration_ms, 2),
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error_message": str(e)})
