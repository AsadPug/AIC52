from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPen, QImage, QPainter, QPixmap, qRgb

from gol_engine import GOLEngine

class GOLLabel(QLabel):
    def __init__(self, engine: GOLEngine, timer: QTimer) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.engine: GOLEngine = engine
        self.timer: QTimer = timer
        self.setMinimumSize(self.engine.width, self.engine.height)
        
        self.image = QImage(engine.width, engine.height, QImage.Format.Format_RGB16)
        self.painter = QPainter(self.image)
        self.pen = QPen(Qt.GlobalColor.white)
        self.pen.setWidth(1)
        self.painter.setPen(self.pen)

    def update(self) -> None:
        self.image.fill(Qt.GlobalColor.black)
        self.draw_image()
        self.setPixmap(
            QPixmap(self.image).scaled(
                self.size().width(), self.size().height(),
                Qt.KeepAspectRatio,
                Qt.fast
            )
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def resize(self) -> None:
        self.painter.end()
        self.image = QImage(self.engine.width, self.engine.height, QImage.Format.Format_Grayscale8)
        self.painter = QPainter(self.image)
        self.painter.setPen(self.pen)
        self.update()

    
    def draw_cells(self) -> None:
        for y in range(self.engine.height):
            for x in range(self.engine.width):
                if self.engine.get_cell_at(x,y) == 1:
                    self.painter.drawPoint(x,y)
    
    def draw_image(self) -> None:
        data = self.engine.data
        gray_color_table = [qRgb(i,i,i) for i in range(256)]
        self.image = QImage((data * 255).data, data.shape[0], data.shape[1],data.strides[0], QImage.Format.Format_Grayscale8 )
        self.image.setColorTable(gray_color_table)
