# Interpreter

Offline screen translator for Japanese retro games. Captures text from any window, performs OCR, translates to English, and displays subtitles in a floating overlay.

![screenshot](screenshot.png)

## Features

- **Fully offline** - No cloud APIs, no internet required after setup
- **Free** - No API costs or subscriptions
- **Private** - Text never leaves your machine
- **Optimized for retro games** - Uses MeikiOCR, trained specifically on Japanese game text
- **Two overlay modes** - Banner (subtitle bar) or inplace (text over game)
- **Translation caching** - Fuzzy matching avoids re-translating similar text
- **Multi-display support** - Overlay appears on the same display as the game

## Requirements

- **Windows 10 version 1903+**, macOS, or Linux (X11/XWayland/Wayland)

### Linux Notes

- **Global hotkeys** require `input` group membership. The installer will show instructions.
- **Native Wayland capture** requires GStreamer PipeWire plugin. The installer will attempt to install it automatically.
- **Inplace overlay** on Wayland only works with fullscreen windows (Wayland's security model prevents knowing window positions).

## Installation

### One-liner Install

**macOS/Linux:**
```bash
curl -LsSf https://raw.githubusercontent.com/bquenin/interpreter/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://raw.githubusercontent.com/bquenin/interpreter/main/install.ps1 | iex"
```

Then run with `interpreter-v2`.

## Upgrading

To update to the latest version, run the installer again (see Installation above).

## Uninstalling

**macOS/Linux:**
```bash
curl -LsSf https://raw.githubusercontent.com/bquenin/interpreter/main/uninstall.sh | bash
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://raw.githubusercontent.com/bquenin/interpreter/main/uninstall.ps1 | iex"
```

This removes interpreter-v2, config files, and cached models.

## Usage

```bash
interpreter-v2
```

This opens the GUI where you can select a window to capture and configure all settings.

## Overlay Modes

### Banner Mode (default)
A subtitle bar at the bottom of the screen displaying translated text. Draggable, opaque background, centered text.

### Inplace Mode
Transparent overlay positioned over the game window. Translated text appears directly over the original Japanese text at OCR-detected positions. Click-through so you can interact with the game.

## How It Works

1. **Screen Capture** - Captures the target window at the configured refresh rate
2. **OCR** - [MeikiOCR](https://github.com/rtr46/meikiocr) extracts Japanese text (optimized for pixel fonts)
3. **Translation** - [Sugoi V4](https://huggingface.co/entai2965/sugoi-v4-ja-en-ctranslate2) translates Japanese to English
4. **Display** - Shows translated text in the selected overlay mode

## Troubleshooting

### Poor OCR accuracy
Try adjusting the OCR confidence slider in the GUI. Lower values include more text (but may include garbage), higher values are stricter.

### Slow performance
First run downloads models (~1.5GB). Subsequent runs use cached models from `~/.cache/huggingface/`.

---

## Fork / Local Development

This section covers installing and running from a local fork of this repo instead of the published PyPI package.

### Prerequisites

Install `uv` if not already installed:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Restart your terminal after installing.

### Redirect installs to a custom drive (optional)

By default uv and HuggingFace store data on C:/. Run this once to redirect everything to a different drive:
```powershell
[System.Environment]::SetEnvironmentVariable("UV_CACHE_DIR",          "X:\uv\cache",  "User")
[System.Environment]::SetEnvironmentVariable("UV_TOOL_DIR",           "X:\uv\tools",  "User")
[System.Environment]::SetEnvironmentVariable("UV_PYTHON_INSTALL_DIR", "X:\uv\python", "User")
[System.Environment]::SetEnvironmentVariable("HF_HUB_CACHE",          "X:\models",    "User")
```
Replace `X:` with your preferred drive. Open a new terminal after running so the values take effect.

### Install from local fork

```powershell
uv tool install --force --python 3.12 "path\to\your\fork"
```

> If env vars aren't loading in the current session, set them inline before the install command:
> ```powershell
> $env:UV_CACHE_DIR = "X:\uv\cache"; $env:UV_TOOL_DIR = "X:\uv\tools"; $env:UV_PYTHON_INSTALL_DIR = "X:\uv\python"; uv tool install --force --python 3.12 "path\to\your\fork"
> ```

### Running the app

Option 1 — double-click `run.bat` in the repo root (sets env vars automatically).

Option 2 — from a terminal:
```powershell
interpreter-v2
```

### Upgrade after code changes

```powershell
uv tool install --force --python 3.12 "path\to\your\fork"
```

### Uninstall

```powershell
uv tool uninstall interpreter-v2
```

To also remove all downloaded packages and models:
```powershell
Remove-Item -Recurse -Force "$env:UV_TOOL_DIR"
Remove-Item -Recurse -Force "$env:UV_CACHE_DIR"
Remove-Item -Recurse -Force "$env:UV_PYTHON_INSTALL_DIR"
Remove-Item -Recurse -Force "$env:HF_HUB_CACHE"
```

### Custom model storage path

Edit `set_models_dir()` in `src/interpreter/__main__.py` to point to any directory:

```python
set_models_dir(r"X:\your\preferred\path")
```

Models are downloaded on **first launch** and reused from cache on all subsequent runs.
