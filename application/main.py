import sys
import cv2
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = None
        self.initUI()

    def initUI(self):
        # tombol Load
        self.load_button = QPushButton('Load', self)
        self.load_button.move(10, 10)
        self.load_button.clicked.connect(self.load_image)

        # tombol Reset
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.move(100, 10)
        self.reset_button.clicked.connect(self.reset_image)

        # tombol start
        self.start_button = QPushButton('Start', self)
        self.start_button.move(10, 540)
        self.start_button.clicked.connect(self.processImage)

        # view 1
        self.view1 = QLabel(self)
        self.view1.setGeometry(10, 50, 780, 520)
        self.scroll(self.view1, 10, 50)

        # view 2
        self.view2 = QLabel(self)
        self.view2.setGeometry(660, 50, 780, 520)
        self.scroll(self.view2, 660, 50)
     
        self.setGeometry(100, 100, 1310, 580)
        self.setWindowTitle('OpenCV Image Viewer')
        self.show()

    def scroll(self, widget, width, height):
        # membuat tampilan scrollable untuk label gambar
        
        scroll = QScrollArea(self)
        scroll.setWidget(widget)
        scroll.setAlignment(Qt.AlignCenter)
        scroll.setWidgetResizable(True)
        scroll.move(width, height)
        scroll.resize(self.width()-4, self.height()-4)
        
        # menambahkan border pada tampilan scrollable
        self.border_color = "black"
        self.border_size = 2
        self.setStyleSheet("QScrollArea {border: %dpx solid %s;}" % (self.border_size, self.border_color))

    def load_image(self):
        # Membuka dialog untuk memilih gambar
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            # Membaca gambar menggunakan OpenCV
            self.image = cv2.imread(fname)
            # Mengonversi gambar ke format yang bisa ditampilkan di Qt
            height, width, channels = self.image.shape
            bytesPerLine = channels * width
            q_image = QImage(self.image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

            # Menampilkan gambar di view
            q_pixmap = QPixmap.fromImage(q_image)
            q_pixmap = q_pixmap.scaled(780, 520, Qt.KeepAspectRatio)         
            self.view1.setPixmap(q_pixmap)
    
    def reset_image(self):
        # Menghapus gambar dari view
        self.view1.setPixmap(QPixmap())
        self.view2.setPixmap(QPixmap())
        self.image = None
    
    def processImage(self):
        # Mengubah gambar menjadi abu-abu dan menampilkannya di view2
        if self.image is not None:
            self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            gray_rgb_image = cv2.cvtColor(self.gray_image, cv2.COLOR_GRAY2RGB)
            height, width, channel = gray_rgb_image.shape
            bytes_per_line = 3 * width
            q_image = QImage(gray_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.view2.setPixmap(QPixmap.fromImage(q_image))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
