import sys
import cv2
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        
        # Membuat tampilan GUI
        self.initUI()
        
        # Membuat variabel untuk menyimpan gambar
        self.original_image = None
        self.gray_image = None
        
    def initUI(self):
        # Membuat tombol untuk memilih gambar
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.loadImage)
        
        # Membuat view untuk menampilkan gambar
        self.view1 = QLabel()
        self.view2 = QLabel()
        
        # Membuat tombol untuk memproses gambar menjadi abu-abu
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.processImage)
        
        # Membuat tombol untuk mereset gambar
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.resetImage)
        
        # Menambahkan elemen-elemen GUI ke dalam layout
        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.view1)
        layout.addWidget(self.start_button)
        layout.addWidget(self.view2)
        layout.addWidget(self.reset_button)
        self.setLayout(layout)
        
        # Mengatur ukuran jendela
        self.setGeometry(100, 100, 400, 400)
        
    def loadImage(self):
        # Memilih gambar dari file dialog
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_path = file_dialog.getOpenFileName()[0]
        
        # Membaca gambar dari file dan menampilkannya di view1
        self.original_image = cv2.imread(file_path)
        rgb_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.view1.setPixmap(QPixmap.fromImage(q_image))
        
    def processImage(self):
        # Mengubah gambar menjadi abu-abu dan menampilkannya di view2
        if self.original_image is not None:
            self.gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            gray_rgb_image = cv2.cvtColor(self.gray_image, cv2.COLOR_GRAY2RGB)
            height, width, channel = gray_rgb_image.shape
            bytes_per_line = 3 * width
            q_image = QImage(gray_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.view2.setPixmap(QPixmap.fromImage(q_image))
        
    def resetImage(self):
        # Menghapus gambar dari view1 dan view2
        self.view1.clear()
        self.view2.clear()
        self.original_image = None
        self.gray_image = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    ex.show()
    sys.exit(app.exec_())
