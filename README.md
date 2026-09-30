# PixelForge 🖼️ ➔ 📐 🗜️

基于 **VTracer (Rust 矢量化算法)** 与 **Pillow (libwebp)** 的高保真图像转换与优化工作台，由 **uv** 现代 Python 工具链全流程管理。

通过轻量现代的 Web 界面，提供：
1. **PNG ➔ SVG 矢量化转换**（无限缩放不失真，适合图标、Logo、插画、线稿）
2. **PNG ➔ WebP 网页极限压缩**（保留 Alpha 透明通道，体积直降 60%~90%）
3. **可视化拖拽调参工作台**（支持拖拽上传、剪贴板粘贴、参数滑块联动、左右分屏实时对比与一键下载）

---

## 🚀 启动与开发

### 1. 一键运行（生产/一体化模式）
只需一行命令即可启动完整的 PixelForge 交互工作台（自动加载构建好的前端 UI 并打开浏览器）：

```bash
uv run pixelforge
```
或者：
```bash
uv run python main.py
```

服务启动后将自动在浏览器打开 `http://127.0.0.1:8000`。

---

### 2. 前后端独立开发（HMR 热重载模式）

本项目采用前后端完全分离架构：

* **启动后端 API 服务**：
  ```bash
  uv run pixelforge --no-open-browser
  ```
  API 运行在 `http://127.0.0.1:8000`，支持 OpenAPI Swagger 交互文档：`http://127.0.0.1:8000/docs`。

* **启动前端开发环境（Vite + Vue 3 + TS）**：
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
  前端开发服务运行在 `http://localhost:5173`，并通过 Vite Proxy 自动转发 `/api` 请求至后端。

* **构建前端产物**：
  ```bash
  cd frontend
  npm run build
  ```
  构建产物将自动输出到 `src/pixelforge/static/`，供后端直接打包分发。

---

## 🐍 Python 代码调用

支持在其他 Python 脚本中直接引入并调用核心算法：

```python
from pixelforge import convert_image, convert_image_to_webp, PresetType

# 1. 转换为 SVG
svg_res = convert_image("logo.png", "logo.svg", preset=PresetType.ICON)
print(f"SVG 耗时: {svg_res.duration_ms:.1f}ms, 大小: {svg_res.output_size_bytes}B")

# 2. 转换为 WebP
webp_res = convert_image_to_webp("photo.png", "photo.webp", quality=80)
print(f"WebP 压缩减少了: {webp_res.reduction_percentage:.1f}%, 耗时: {webp_res.duration_ms:.1f}ms")
```

---

## 📁 项目结构

```
PixelForge/
├── frontend/                     # 🎨 独立前端工程 (Vue 3 + TS + Vite + Tailwind CSS)
│   ├── src/
│   │   ├── api/client.ts         # REST API 请求客户端
│   │   ├── components/           # 组件拆分 (Header, DropZone, Controls, Previewer)
│   │   ├── types/                # TypeScript 接口与类型定义
│   │   ├── App.vue               # 顶层应用组件
│   │   ├── main.ts               # 前端入口
│   │   └── style.css             # Tailwind 样式与原子类
│   ├── package.json
│   ├── vite.config.ts            # Vite 代理与打包配置
│   └── tsconfig.json
│
├── src/
│   └── pixelforge/               # ⚙️ 独立后端服务 (FastAPI + VTracer + Pillow)
│       ├── __init__.py           # 顶层 Python API 导出
│       ├── presets.py            # 场景化调优预设
│       ├── converter.py          # SVG 矢量化转换引擎 (VTracer)
│       ├── webp_converter.py     # WebP 压缩转换引擎 (Pillow)
│       ├── server.py             # FastAPI REST API 路由与静态挂载
│       ├── cli.py                # CLI 工作台启动器
│       └── static/               # 前端构建产物 (dist assets)
│
├── pyproject.toml                # Python 项目与 uv 依赖配置
├── uv.lock                       # 依赖锁定
├── LICENSE                       # Apache-2.0 开源协议
├── README.md                     # 项目说明文档
└── main.py                       # 顶层一键启动入口
```

---

## 📄 开源协议

本项目采用 [Apache-2.0 License](LICENSE) 开源协议。

