from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QImage, QPainter, QPixmap, QPalette, qRgb

from gol_engine import GOLEngine

class GOLWidget(QWidget):
    def __init__(self, engine: GOLEngine) -> None:
        super().__init__()
    
        self.engine: GOLEngine = engine
        self.main_layout = QVBoxLayout()
        self.gol_label = QLabel()
        self.gol_label.setMinimumSize(self.engine.width, self.engine.height)
        self.gol_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image = QImage(engine.width, engine.height, QImage.Format.Format_RGB16)

        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.gol_label)
        
        self.set_background_color()

        self.painter = QPainter(self.image)
        self.pen = QPen(Qt.GlobalColor.white)
        self.pen.setWidth(1)
        self.painter.setPen(self.pen)

    def update(self) -> None:
        self.image.fill(Qt.GlobalColor.black)
        self.draw_image()
        self.gol_label.setPixmap(
            QPixmap(self.image).scaled(
                self.gol_label.size().width(), self.gol_label.size().height(),
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )
        )
        self.gol_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def resize(self) -> None:
        self.painter.end()
        self.image = QImage(self.engine.width, self.engine.height, QImage.Format.Format_RGB16)
        self.painter = QPainter(self.image)
        self.painter.setPen(self.pen)
        self.update()

    
    def draw_cells(self) -> None:
        for y in range(self.engine.height):
            for x in range(self.engine.width):
                if self.engine.get_cell_at(x,y) is True:
                    self.painter.drawPoint(x,y)

    def draw_image(self) -> None:
        data = self.engine.data
        gray_color_table = [qRgb(i,i,i) for i in range(256)]
        self.image = QImage((data * 255).data, data.shape[0], data.shape[1],data.strides[0], QImage.Format.Format_Grayscale8 )
        self.image.setColorTable(gray_color_table)
    
    def set_background_color(self) -> None:
        self.bg_palette = QPalette()
        self.bg_palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.gray)
        self.setAutoFillBackground(True)
        self.setPalette(self.bg_palette)