import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import Qt, QRectF

from model import Grid
class Vue(QMainWindow):
    def __init__(self, grid: Grid) ->None:
        super().__init__()
        self.window_width = 800    
        self.window_height = 800
        self.setWindowTitle("Game of life")
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMaximumSize(self.window_width, self.window_height)
        
        self.grid = grid

        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view = QGraphicsView(self.graphics_scene, self)
        self.graphics_view.setGeometry(0, 0, self.window_width, self.window_height)

        
        self.white_brush = QBrush(Qt.GlobalColor.white)
        self.grey_pen = QPen(Qt.GlobalColor.gray)
        

    def update_gui(self) -> None:
        self.graphics_scene.clear()
        self.draw_background()
        self.draw_cells()
        self.graphics_view.fitInView(self.graphics_scene.itemsBoundingRect())


    def draw_background(self) -> None:
        rect = QGraphicsRectItem(0, 0, self.window_width, self.window_height)
        rect.setBrush(Qt.GlobalColor.black)
        self.graphics_scene.addItem(rect)

    def draw_cell_at(self, x: int, y: int):
        cell_width = self.window_width / self.grid.width
        cell_height = self.window_height / self.grid.height

        rect = QGraphicsRectItem(
            x * cell_width, y * cell_height,
            cell_width, cell_height
        )

        rect.setBrush(self.white_brush)
        rect.setPen(self.grey_pen)
        self.graphics_scene.addItem(rect)

    def draw_cells(self) -> None:
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.get_cell_at(x,y) is True:
                    self.draw_cell_at(x,y)
        
  


        
        