from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QApplication, QGraphicsView
from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import Qt, QTimer
import sys
from time import sleep


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Pyside graphics view")
        self.setGeometry(300,200,640,520)
        self.create_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.new_ellipse)

    def create_ui(self):
        self.scene = QGraphicsScene(self)
        self.green_brush = QBrush(Qt.GlobalColor.green)
        self.blue_brush = QBrush(Qt.GlobalColor.blue)

        self.black_pen = QPen(Qt.GlobalColor.black)
        self.black_pen.setWidth(5)

        ellipse = self.scene.addEllipse(10,10,200,200, self.black_pen, self.green_brush)

        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0,0,640,640)

    def new_ellipse(self):
        self.scene.clear()
        ellipse2 = self.scene.addEllipse(0,0,150,150, self.black_pen, self.blue_brush)

app = QApplication(sys.argv)
window = Window()
window.timer.start(3000)
window.show()
app.exec()

