import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen 
from PySide6.QtCore import Qt, QTimer

from model import Grid
class Vue(QGraphicsView):
    def __init__(self, grid: Grid) ->None:
        super().__init__()
        self.grahics_scene = QGraphicsScene()
        self.setScene(self.grahics_scene)

    def update_gui(self) -> None:
        self.draw_cell_at(0,0)

    def draw_cell_at(self, x: int, y: int):
        rect = QGraphicsRectItem(x, y, 1, 1)
        rect.setBrush(QBrush(Qt.GlobalColor.black))
        self.grahics_scene.addItem(rect)
  


        
        