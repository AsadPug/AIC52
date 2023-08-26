import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QBrush, QPen 
from PySide6.QtCore import Qt, QTimer

class Vue(QMainWindow):
    def __init__(self, w_width: int, w_height: int) ->None:
        scene = QGraphicsScene()
        graphics_view = QGraphicsView()
        self.geometry(0, 0, w_width, w_height)
    
        self.show()

    def update_gui(self) -> None:
        pass
        
        