import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QFileDialog, QHBoxLayout, QVBoxLayout,
    QScrollArea, QFrame, QSizePolicy, QGraphicsDropShadowEffect,
    QStatusBar, QApplication
)
from PyQt5.QtGui import (
    QImage, QPixmap, QFont, QColor, QPalette,
    QLinearGradient, QPainter, QFontDatabase
)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from filters import FILTERS


# ── Colour palette ─────────────────────────────────────────────
BG_DEEP    = "#07080f"
BG_PANEL   = "#0d0f1c"
BG_CARD    = "#12152a"
ACCENT_1   = "#7b5ea7"   # violet
ACCENT_2   = "#00d4ff"   # cyan
ACCENT_HOT = "#ff2d78"   # hot pink
TEXT_MAIN  = "#e8eaf6"
TEXT_DIM   = "#5a6080"
BORDER     = "#1e2240"


STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG_DEEP};
    color: {TEXT_MAIN};
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}}

/* ── TOP BAR ── */
#topBar {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {BG_PANEL}, stop:1 #0a0c18);
    border-bottom: 1px solid {BORDER};
    padding: 0 24px;
}}
#appTitle {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 3px;
    color: {ACCENT_2};
}}
#appSub {{
    font-size: 11px;
    color: {ACCENT_1};
    letter-spacing: 2px;
}}

/* ── BUTTONS ── */
QPushButton {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_MAIN};
    background: {BG_CARD};
    letter-spacing: 0.5px;
}}
QPushButton:hover {{
    border-color: {ACCENT_2};
    color: {ACCENT_2};
    background: #151930;
}}
QPushButton:pressed {{
    background: #0e1122;
}}
#btnLoad {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {ACCENT_1}, stop:1 #5c3d8f);
    border: none;
    color: white;
    padding: 12px 28px;
    font-size: 14px;
}}
#btnLoad:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #9b7ec7, stop:1 {ACCENT_1});
}}
#btnSave {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {ACCENT_HOT}, stop:1 #b01f56);
    border: none;
    color: white;
    padding: 12px 28px;
    font-size: 14px;
}}
#btnSave:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #ff5599, stop:1 {ACCENT_HOT});
}}
#btnSave:disabled {{
    background: {BG_CARD};
    color: {TEXT_DIM};
    border: 1px solid {BORDER};
}}

/* ── FILTER BUTTONS ── */
#filterBtn {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 12px;
    color: {TEXT_DIM};
    text-align: left;
    min-width: 140px;
}}
#filterBtn:hover {{
    border-color: {ACCENT_1};
    color: {TEXT_MAIN};
    background: #161830;
}}
#filterBtn[active="true"] {{
    border-color: {ACCENT_2};
    color: {ACCENT_2};
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #0d1525, stop:1 #0a1020);
    font-weight: 700;
}}

/* ── IMAGE FRAME ── */
#imageFrame {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
}}
#imageLabel {{
    color: {TEXT_DIM};
    font-size: 15px;
    letter-spacing: 1px;
}}

/* ── SIDEBAR ── */
#sidebar {{
    background: {BG_PANEL};
    border-left: 1px solid {BORDER};
    min-width: 180px;
    max-width: 200px;
}}
#sidebarTitle {{
    font-size: 10px;
    letter-spacing: 3px;
    color: {TEXT_DIM};
    padding: 18px 16px 8px 16px;
}}

/* ── STATUS BAR ── */
QStatusBar {{
    background: {BG_PANEL};
    color: {TEXT_DIM};
    font-size: 11px;
    border-top: 1px solid {BORDER};
    padding: 0 16px;
}}

/* ── SCROLL AREA ── */
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {BG_DEEP};
    width: 6px;
    margin: 0;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {ACCENT_1};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
"""


class DropImageLabel(QLabel):
    """Central image display that also accepts drag‑and‑drop."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("imageLabel")
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self._drop_cb = None
        self._set_placeholder()

    def set_drop_callback(self, cb):
        self._drop_cb = cb

    def _set_placeholder(self):
        self.setText("drag & drop an image here\nor click  ✦ Load Image")

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        if urls and self._drop_cb:
            self._drop_cb(urls[0].toLocalFile())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PixelPopp ✦")
        self.resize(1280, 800)
        self.setMinimumSize(960, 640)
        self.setStyleSheet(STYLESHEET)

        self._original_image  = None   # numpy BGR
        self._displayed_image = None
        self._active_filter   = "✦ Original"
        self._filter_buttons  = {}

        self._build_ui()
        self._connect_signals()
        self._status("Ready  ·  Load an image to begin")

    # ── BUILD ──────────────────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setSpacing(0)
        root_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(self._make_top_bar())

        # body: image area + sidebar
        body = QHBoxLayout()
        body.setSpacing(0)
        body.setContentsMargins(0, 0, 0, 0)
        body.addWidget(self._make_image_area(), 1)
        body.addWidget(self._make_sidebar())

        body_widget = QWidget()
        body_widget.setLayout(body)
        root_layout.addWidget(body_widget, 1)

        self.setStatusBar(QStatusBar())

    def _make_top_bar(self):
        bar = QFrame()
        bar.setObjectName("topBar")
        bar.setFixedHeight(64)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(24, 0, 24, 0)

        # title block
        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        t = QLabel("PIXELPOPP")
        t.setObjectName("appTitle")
        s = QLabel("IMAGE STUDIO")
        s.setObjectName("appSub")
        title_col.addWidget(t)
        title_col.addWidget(s)
        layout.addLayout(title_col)
        layout.addStretch()

        # action buttons
        self.btn_load = QPushButton("✦  Load Image")
        self.btn_load.setObjectName("btnLoad")
        self.btn_load.setCursor(Qt.PointingHandCursor)

        self.btn_save = QPushButton("↓  Save Image")
        self.btn_save.setObjectName("btnSave")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setEnabled(False)

        layout.addWidget(self.btn_load)
        layout.addSpacing(10)
        layout.addWidget(self.btn_save)
        return bar

    def _make_image_area(self):
        frame = QFrame()
        frame.setObjectName("imageFrame")
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(16, 16, 16, 16)

        self.image_label = DropImageLabel()
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.set_drop_callback(self._load_file)
        lay.addWidget(self.image_label)
        return frame

    def _make_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(10, 0, 10, 16)
        lay.setSpacing(6)

        heading = QLabel("FILTERS")
        heading.setObjectName("sidebarTitle")
        lay.addWidget(heading)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        inner = QWidget()
        self._filter_layout = QVBoxLayout(inner)
        self._filter_layout.setSpacing(5)
        self._filter_layout.setContentsMargins(0, 0, 0, 0)

        for name in FILTERS:
            btn = QPushButton(name)
            btn.setObjectName("filterBtn")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(False)
            btn.clicked.connect(lambda _, n=name: self._apply_filter(n))
            self._filter_buttons[name] = btn
            self._filter_layout.addWidget(btn)

        self._filter_layout.addStretch()
        scroll.setWidget(inner)
        lay.addWidget(scroll, 1)

        self._mark_active("✦ Original")
        return sidebar

    # ── SIGNALS ───────────────────────────────────────────────

    def _connect_signals(self):
        self.btn_load.clicked.connect(self._open_dialog)
        self.btn_save.clicked.connect(self._save_image)

    # ── LOAD ──────────────────────────────────────────────────

    def _open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff *.webp)"
        )
        if path:
            self._load_file(path)

    def _load_file(self, path: str):
        img = cv2.imdecode(
            np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR
        )
        if img is None:
            self._status(f"⚠  Could not open: {path}")
            return
        self._original_image = img
        self._active_filter  = "✦ Original"
        self._mark_active("✦ Original")
        self._display(img)
        self.btn_save.setEnabled(True)
        fname = os.path.basename(path)
        h, w  = img.shape[:2]
        self._status(f"Loaded  ·  {fname}  ·  {w} × {h} px")

    # ── FILTERS ───────────────────────────────────────────────

    def _apply_filter(self, name: str):
        if self._original_image is None:
            self._status("⚠  Load an image first")
            return
        fn  = FILTERS[name]
        out = fn(self._original_image)
        self._display(out)
        self._displayed_image = out
        self._active_filter   = name
        self._mark_active(name)
        self._status(f"Filter applied  ·  {name}")

    def _mark_active(self, name: str):
        for n, btn in self._filter_buttons.items():
            btn.setProperty("active", str(n == name).lower())
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ── DISPLAY ───────────────────────────────────────────────

    def _display(self, img: np.ndarray):
        self._displayed_image = img
        rgb   = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg  = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix   = QPixmap.fromImage(qimg)
        avail = self.image_label.size()
        scaled = pix.scaled(avail, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self._displayed_image is not None:
            self._display(self._displayed_image)

    # ── SAVE ──────────────────────────────────────────────────

    def _save_image(self):
        if self._displayed_image is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "pixelpopp_export.png",
            "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)"
        )
        if path:
            ext = os.path.splitext(path)[1].lower()
            params = [cv2.IMWRITE_PNG_COMPRESSION, 9] if ext == ".png" else \
                     [cv2.IMWRITE_JPEG_QUALITY, 97]
            cv2.imencode(ext, self._displayed_image, params)[1].tofile(path)
            self._status(f"Saved  ·  {os.path.basename(path)}")

    # ── HELPERS ───────────────────────────────────────────────

    def _status(self, msg: str):
        self.statusBar().showMessage(f"  {msg}")