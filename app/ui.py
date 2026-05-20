import sys
import cv2

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QScrollArea
)

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import filters


class PixelPopp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PixelPopp ✨")
        self.setGeometry(100, 100, 1200, 700)

        self.image = None
        self.processed = None

        self.setup_ui()

    def setup_ui(self):

        main_layout = QHBoxLayout()

        # LEFT PANEL
        left_layout = QVBoxLayout()

        upload_btn = QPushButton("Upload Image")
        upload_btn.clicked.connect(self.load_image)

        save_btn = QPushButton("Save Image")
        save_btn.clicked.connect(self.save_image)

        left_layout.addWidget(upload_btn)
        left_layout.addWidget(save_btn)

        # FILTER BUTTONS
        filter_buttons = [
            ("Grayscale", filters.grayscale),
            ("Blur", filters.gaussian_blur),
            ("Edges", filters.edge_detection),
            ("Sketch", filters.pencil_sketch),
            ("Cartoon", filters.cartoon_filter),
            ("Neon Glow", filters.neon_glow),
            ("Midnight Blue", filters.midnight_blue),
            ("Neo Tokyo", filters.neo_tokyo),
            ("Retro Film", filters.retro_film)
        ]

        for name, func in filter_buttons:
            btn = QPushButton(name)

            btn.clicked.connect(
                lambda checked, f=func: self.apply_filter(f)
            )

            left_layout.addWidget(btn)

        main_layout.addLayout(left_layout)

        # IMAGE AREA
        self.image_label = QLabel()

        self.image_label.setAlignment(Qt.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidget(self.image_label)
        scroll.setWidgetResizable(True)

        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def load_image(self):

        file_path, _ = QFileDialog.getOpenFileName()

        if file_path:

            self.image = cv2.imread(file_path)

            self.processed = self.image.copy()

            self.display_image(self.image)

    def display_image(self, image):

        if len(image.shape) == 2:
            qformat = QImage.Format_Grayscale8

        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            qformat = QImage.Format_RGB888

        h, w = image.shape[:2]

        bytes_per_line = image.strides[0]

        qimg = QImage(
            image.data,
            w,
            h,
            bytes_per_line,
            qformat
        )

        pixmap = QPixmap.fromImage(qimg)

        self.image_label.setPixmap(pixmap)

    def apply_filter(self, filter_function):

        if self.image is None:
            QMessageBox.warning(self, "Error", "Upload an image first.")
            return

        self.processed = filter_function(self.image.copy())

        self.display_image(self.processed)

    def save_image(self):

        if self.processed is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG Files (*.png);;JPG Files (*.jpg)"
        )

        if file_path:
            cv2.imwrite(file_path, self.processed)


def run():
    app = QApplication(sys.argv)

    window = PixelPopp()

    window.show()

    sys.exit(app.exec_())