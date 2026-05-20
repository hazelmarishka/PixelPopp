import cv2
import numpy as np


# ---------------- BASIC FILTERS ---------------- #

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def gaussian_blur(image):
    return cv2.GaussianBlur(image, (15, 15), 0)


def edge_detection(image):
    return cv2.Canny(image, 100, 200)


def pencil_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    inverted = 255 - gray

    blur = cv2.GaussianBlur(inverted, (21, 21), 0)

    inverted_blur = 255 - blur

    sketch = cv2.divide(gray, inverted_blur, scale=256.0)

    return sketch


def cartoon_filter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9
    )

    color = cv2.bilateralFilter(image, 9, 250, 250)

    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon


# ---------------- CINEMATIC FILTERS ---------------- #

def neon_glow(image):
    glow = cv2.GaussianBlur(image, (0, 0), 10)

    blended = cv2.addWeighted(image, 1.2, glow, 0.5, 0)

    pink_tint = np.full_like(blended, (30, 0, 40))

    return cv2.add(blended, pink_tint)


def midnight_blue(image):
    blue_tint = np.full_like(image, (40, 20, 0))

    cool = cv2.add(image, blue_tint)

    hsv = cv2.cvtColor(cool, cv2.COLOR_BGR2HSV)

    hsv[:, :, 1] = hsv[:, :, 1] * 0.5

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def neo_tokyo(image):
    enhanced = cv2.convertScaleAbs(image, alpha=1.4, beta=20)

    tint = np.full_like(enhanced, (40, 0, 60))

    return cv2.add(enhanced, tint)


def retro_film(image):
    kernel = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])

    sepia = cv2.transform(image, kernel)

    sepia = np.clip(sepia, 0, 255).astype(np.uint8)

    noise = np.random.normal(0, 15, sepia.shape).astype(np.uint8)

    return cv2.add(sepia, noise)