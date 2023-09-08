from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QImage, QPainter, QPixmap

from model import GOLEngine

class GOLLabel(QLabel):
    def __init__(self, engine: GOLEngine) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.engine: GOLEngine = engine
        self.setMinimumSize(self.engine.width, self.engine.height)
        
        self.image = QImage(engine.width, engine.height, QImage.Format.Format_RGB16)
        self.painter = QPainter(self.image)
        self.pen = QPen(Qt.GlobalColor.white)
        self.pen.setWidth(1)
        self.painter.setPen(self.pen)

    def update(self) -> None:
        self.image.fill(Qt.GlobalColor.black)
        self.draw_cells()
        self.setPixmap(
            QPixmap(self.image).scaled(
                self.size().width(), self.size().height(),
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def draw_cells(self) -> None:
        for y in range(self.engine.height):
            for x in range(self.engine.width):
                if self.engine.get_cell_at(x,y) is True:
                    self.painter.drawPoint(x,y)