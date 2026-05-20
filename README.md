# PixelPopp☆

A modern desktop image processing application built with Python, OpenCV, and PyQt5.

---

## Features

### Basic Filters
- Grayscale
- Gaussian Blur
- Edge Detection
- Pencil Sketch
- Cartoon Filter

### Cinematic Filters
- Neon Glow
- Midnight Blue
- Neo Tokyo
- Retro Film

---

## Tech Stack

- Python
- OpenCV
- PyQt5
- NumPy
- Pillow

---

## Project Structure

```text
PixelPopp/
│
├── app/
│   ├── main.py
│   ├── ui.py
│   └── filters.py
│
├── screenshots/
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/PixelPopp.git
```

### 2. Go into the project folder

```bash
cd PixelPopp
```

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Activate virtual environment

#### Windows CMD

```bash
venv\Scripts\activate
```

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
cd app
python main.py
```

---

## Filters Included

| Filter | Description |
|---|---|
| Grayscale | Converts image to black and white |
| Gaussian Blur | Smooth blur effect |
| Edge Detection | Detects image outlines |
| Pencil Sketch | Sketch drawing effect |
| Cartoon Filter | Cartoon-style processing |
| Neon Glow | Bright cinematic glow |
| Midnight Blue | Cool blue cinematic tone |
| Neo Tokyo | Cyberpunk-inspired filter |
| Retro Film | Vintage sepia film effect |

---

## Concepts Learned

This project teaches:

- Image processing fundamentals
- RGB color manipulation
- OpenCV basics
- GUI development with PyQt5
- Image filtering techniques
- File handling in Python
- Real-time image rendering

---

## Future Improvements

- Webcam filters
- Real-time video effects
- Face detection
- Gesture controls
- AI enhancement filters
- Filter intensity sliders
- Drag and drop image upload

---

## Known Issues

- OpenCV may struggle with image paths containing special Unicode characters on Windows.
- Using simple folder paths is recommended.

Example:

```text
D:\Images
```

instead of:

```text
D:\✮ blingg blingg ✮
```

---

## Author

Built by hazelll☆

---

## License

This project is licensed under the MIT License.