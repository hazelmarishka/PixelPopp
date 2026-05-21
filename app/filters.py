import cv2
import numpy as np

def apply_none(image):
    """Return original image unchanged."""
    return image.copy()

def apply_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def apply_gaussian_blur(image):
    return cv2.GaussianBlur(image, (21, 21), 0)

def apply_edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 180)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def apply_pencil_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    sketch = cv2.divide(gray, blur, scale=256.0)
    sketch = cv2.equalizeHist(sketch)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

def apply_cartoon(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(image, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# ── CINEMATIC FILTERS ──────────────────────────────────────────

def apply_neon_glow(image):
    """Hot‑pink / cyan neon on dark base."""
    dark = (image * 0.35).astype(np.uint8)
    blur = cv2.GaussianBlur(image, (0, 0), 12)
    b, g, r = cv2.split(blur)
    b = np.clip(b.astype(np.int32) * 2, 0, 255).astype(np.uint8)
    r = np.clip(r.astype(np.int32) * 1, 0, 255).astype(np.uint8)
    g = np.clip(g.astype(np.int32) * 1, 0, 255).astype(np.uint8)
    glow = cv2.merge([b, g, r])
    result = cv2.addWeighted(dark, 0.55, glow, 0.75, 0)
    return result

def apply_midnight_blue(image):
    """Deep ethereal blue — cool shadows, lifted midtones, no red bleed."""
    img = image.astype(np.float32)
    b, g, r = cv2.split(img)

    # push blue channel up, pull red way down, desaturate green slightly
    r = np.clip(r * 0.45 - 10, 0, 255)
    g = np.clip(g * 0.70 + 5,  0, 255)
    b = np.clip(b * 1.35 + 40, 0, 255)

    result = cv2.merge([b, g, r]).astype(np.uint8)

    # soft ethereal glow on top
    glow = cv2.GaussianBlur(result, (0, 0), 14)
    result = cv2.addWeighted(result, 0.80, glow, 0.30, 0)

    # blend a tiny bit of original luminance back so details don't vanish
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR).astype(np.float32)
    result = cv2.addWeighted(result, 0.88, gray_3ch.astype(np.uint8), 0.12, 0)

    return result

def apply_neo_tokyo(image):
    """Cyberpunk: magenta + cyan split, halation glow."""
    b, g, r = cv2.split(image.astype(np.float32))
    r = np.clip(r * 1.30 + 20, 0, 255)
    g = np.clip(g * 0.70,       0, 255)
    b = np.clip(b * 1.45 + 30,  0, 255)
    result = cv2.merge([b, g, r]).astype(np.uint8)
    # chromatic aberration
    rows, cols = result.shape[:2]
    M_r = np.float32([[1, 0, 3], [0, 1, 0]])
    M_b = np.float32([[1, 0, -3], [0, 1, 0]])
    rb, rg, rr = cv2.split(result)
    rr = cv2.warpAffine(rr, M_r, (cols, rows))
    rb = cv2.warpAffine(rb, M_b, (cols, rows))
    result = cv2.merge([rb, rg, rr])
    # glow
    glow = cv2.GaussianBlur(result, (0, 0), 8)
    return cv2.addWeighted(result, 0.75, glow, 0.45, 0)

def apply_retro_film(image):
    """Warm sepia + grain + vignette."""
    # sepia
    kernel = np.array([[0.272, 0.534, 0.131],
                        [0.349, 0.686, 0.168],
                        [0.393, 0.769, 0.189]])
    sepia = cv2.transform(image, kernel)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    # grain
    noise = np.random.normal(0, 18, sepia.shape).astype(np.int16)
    sepia = np.clip(sepia.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    # vignette
    rows, cols = sepia.shape[:2]
    k_x = cv2.getGaussianKernel(cols, cols * 0.55)
    k_y = cv2.getGaussianKernel(rows, rows * 0.55)
    vignette = k_y * k_x.T
    vignette = vignette / vignette.max()
    for i in range(3):
        sepia[:, :, i] = (sepia[:, :, i] * vignette).astype(np.uint8)
    return sepia

# ── NEW EXTRA FILTERS ──────────────────────────────────────────

def apply_vaporwave(image):
    """Pastel pink‑to‑purple dreamscape."""
    b, g, r = cv2.split(image.astype(np.float32))
    r = np.clip(r * 1.25 + 40, 0, 255)
    g = np.clip(g * 0.65 + 10, 0, 255)
    b = np.clip(b * 1.50 + 50, 0, 255)
    result = cv2.merge([b, g, r]).astype(np.uint8)
    blur = cv2.GaussianBlur(result, (0, 0), 6)
    return cv2.addWeighted(result, 0.80, blur, 0.40, 0)

def apply_infrared(image):
    """False‑colour infrared: foliage turns white, sky turns dark."""
    b, g, r = cv2.split(image.astype(np.float32))
    new_r = np.clip(g * 1.4,         0, 255)
    new_g = np.clip(r * 0.6 + g * 0.4, 0, 255)
    new_b = np.clip(b * 0.3,         0, 255)
    result = cv2.merge([new_b, new_g, new_r]).astype(np.uint8)
    return cv2.cvtColor(cv2.cvtColor(result, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

def apply_golden_hour(image):
    """Warm sunset tones — lifted shadows, orange cast."""
    b, g, r = cv2.split(image.astype(np.float32))
    r = np.clip(r * 1.20 + 25, 0, 255)
    g = np.clip(g * 1.05 + 10, 0, 255)
    b = np.clip(b * 0.70,       0, 255)
    result = cv2.merge([b, g, r]).astype(np.uint8)
    return result

def apply_glitch(image):
    """RGB channel shift + horizontal scan‑line tears."""
    result = image.copy()
    rows, cols = result.shape[:2]
    # channel shift
    shift = 8
    b, g, r = cv2.split(result)
    r = np.roll(r, shift,  axis=1)
    b = np.roll(b, -shift, axis=1)
    result = cv2.merge([b, g, r])
    # random scan‑line tears
    rng = np.random.default_rng(42)
    for _ in range(12):
        y     = rng.integers(0, rows)
        h     = rng.integers(2, 6)
        dx    = rng.integers(-20, 20)
        strip = result[y:y+h, :, :].copy()
        result[y:y+h, :, :] = np.roll(strip, dx, axis=1)
    return result

def apply_duotone(image):
    """Deep navy → hot coral duotone."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    shadow = np.array([30,  20, 10],  dtype=np.float32)   # deep navy  (BGR)
    hi     = np.array([80, 100, 255], dtype=np.float32)   # hot coral
    out = np.zeros((*gray.shape, 3), dtype=np.float32)
    for c in range(3):
        out[:, :, c] = shadow[c] * (1 - gray) + hi[c] * gray
    return np.clip(out, 0, 255).astype(np.uint8)

# ── FILTER REGISTRY (used by ui.py) ───────────────────────────

FILTERS = {
    "✦ Original":      apply_none,
    "Grayscale":        apply_grayscale,
    "Gaussian Blur":    apply_gaussian_blur,
    "Edge Detection":   apply_edge_detection,
    "Pencil Sketch":    apply_pencil_sketch,
    "Cartoon":          apply_cartoon,
    "Neon Glow":        apply_neon_glow,
    "Midnight Blue":    apply_midnight_blue,
    "Neo Tokyo":        apply_neo_tokyo,
    "Retro Film":       apply_retro_film,
    "Vaporwave":        apply_vaporwave,
    "Infrared":         apply_infrared,
    "Golden Hour":      apply_golden_hour,
    "Glitch":           apply_glitch,
    "Duotone":          apply_duotone,
}