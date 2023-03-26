import cv2
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class CameraViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 700, 550)

        # Inisialisasi kamera
        self.cap = cv2.VideoCapture(0)

        # Buat widget untuk menampilkan gambar
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # Buat tombol start dan stop
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setDisabled(True)

        # Buat layout untuk menempatkan widget
        layout_button = QHBoxLayout()
        layout_button.addWidget(self.start_button)
        layout_button.addWidget(self.stop_button)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(layout_button)
        
        self.setLayout(layout)

    def start(self):
        # Mulai pengambilan gambar
        self.showing = True
        self.start_button.setDisabled(True)
        self.stop_button.setEnabled(True)

        # Set ukuran jendela ke ukuran awal
        self.show_frame()

    def stop(self):
        # Menghentikan pengambilan gambar
        self.showing = False
        self.start_button.setEnabled(True)
        self.stop_button.setDisabled(True)

        # Kembalikan ukuran jendela ke ukuran awal
    def show_frame(self):
        if self.showing:
            # Ambil frame dari kamera
            ret, frame = self.cap.read()

            if ret:
                # Ubah frame menjadi gambar Qt
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = QImage(rgb_image.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(img)

                # Tampilkan gambar di label
                self.label.setPixmap(pixmap)

            # Tampilkan frame berikutnya setelah 10ms
            QTimer.singleShot(10, self.show_frame)

if __name__ == '__main__':
    app = QApplication([])
    viewer = CameraViewer()
    viewer.show()
    app.exec_()
