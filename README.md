# PixelPopp☆

A sleek, cyberpunk-themed desktop image processing application built with Python, OpenCV, and PyQt5. Load any image, apply cinematic and creative filters, and export your result — all inside a dark, neon-lit UI.

---

---

## Features

- Drag & drop image loading (or use the Load button)
- ✦ Original / reset button — remove any filter instantly
- 15 filters across Basic, Cinematic, and Creative categories
- Active filter highlight — always know what's applied
- Unicode-safe file paths (special characters in folder names work fine)
- Export at full quality (PNG, JPEG, BMP)
- Responsive image preview — scales cleanly on any window size

---

## Filters

### Basic
| Filter | Description |
|---|---|
| ✦ Original | Resets to the unedited image |
| Grayscale | Classic black and white conversion |
| Gaussian Blur | Soft smoothing blur |
| Edge Detection | Canny edge outlines |
| Pencil Sketch | Hand-drawn sketch effect |
| Cartoon | Flat-colour cartoon style |

### Cinematic
| Filter | Description |
|---|---|
| Neon Glow | Hot-pink and cyan glow on a dark base |
| Midnight Blue | Deep ethereal blue — cool shadows, lifted midtones |
| Neo Tokyo | Cyberpunk magenta/cyan with chromatic aberration |
| Retro Film | Warm sepia with grain and vignette |

### Creative
| Filter | Description |
|---|---|
| Vaporwave | Pastel pink-to-purple dreamscape |
| Infrared | False-colour infrared rendering |
| Golden Hour | Warm sunset orange tones |
| Glitch | RGB channel shift with scan-line tears |
| Duotone | Deep navy to hot coral two-tone |

---

## Tech Stack

- Python 3.10+
- OpenCV
- PyQt5
- NumPy
- Pillow

---

---

## Features

- Drag & drop image loading (or use the Load button)
- ✦ Original / reset button — remove any filter instantly
- 15 filters across Basic, Cinematic, and Creative categories
- Active filter highlight — always know what's applied
- Unicode-safe file paths (special characters in folder names work fine)
- Export at full quality (PNG, JPEG, BMP)
- Responsive image preview — scales cleanly on any window size

---

## Filters

### Basic
| Filter | Description |
|---|---|
| ✦ Original | Resets to the unedited image |
| Grayscale | Classic black and white conversion |
| Gaussian Blur | Soft smoothing blur |
| Edge Detection | Canny edge outlines |
| Pencil Sketch | Hand-drawn sketch effect |
| Cartoon | Flat-colour cartoon style |

### Cinematic
| Filter | Description |
|---|---|
| Neon Glow | Hot-pink and cyan glow on a dark base |
| Midnight Blue | Deep ethereal blue — cool shadows, lifted midtones |
| Neo Tokyo | Cyberpunk magenta/cyan with chromatic aberration |
| Retro Film | Warm sepia with grain and vignette |

### Creative
| Filter | Description |
|---|---|
| Vaporwave | Pastel pink-to-purple dreamscape |
| Infrared | False-colour infrared rendering |
| Golden Hour | Warm sunset orange tones |
| Glitch | RGB channel shift with scan-line tears |
| Duotone | Deep navy to hot coral two-tone |

---

## Tech Stack

- Python 3.10+
- OpenCV
- PyQt5
- NumPy
- Pillow

---

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/PixelPopp.git
cd PixelPopp
```

### 2. Create and activate a virtual environment

**Windows CMD**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows PowerShell**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
cd app
python main.py
```

---
---

## Usage

1. Click **✦ Load Image** or drag and drop an image onto the canvas
2. Click any filter in the sidebar to apply it instantly
3. Click **✦ Original** to remove the filter and restore your image
4. Click **↓ Save Image** to export — choose PNG, JPEG, or BMP

---

## Known Issues

- Very large images (above ~6000px on either side) may be slow to process on some filters like Gaussian Blur and Retro Film
- On some Linux distros, PyQt5 may need to be installed via your system package manager (`sudo apt install python3-pyqt5`) rather than pip

---

## Concepts Covered

- Image processing fundamentals
- RGB and BGR colour channel manipulation
- OpenCV filter pipelines
- LUT-based colour grading
- Chromatic aberration simulation
- Gaussian glow and vignette compositing
- GUI development with PyQt5
- Drag and drop in Qt
- HiDPI / retina display support

---

## Future Ideas

- Filter intensity sliders
- Real-time webcam filters
- Before / after split-view
- Batch processing multiple images
- AI-based upscaling or style transfer
- Custom filter presets you can save and reload

---

## Author

Built by **hazelll☆**

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
