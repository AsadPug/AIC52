import sys
from PySide6 import QtCore, QtWidgets, QtGui

class Vue:
    def __init__(self, w_width: int, w_height: int) ->None:
        
        gui = QtWidgets.QApplication([])
        main_widget = QtWidgets.QWidget()
        graphics_view = QtWidgets.QGraphicsView()
        graphics_view.resize(w_width, w_height)
        main_widget.resize(w_width, w_height)
        rect = QtWidgets.QGraphicsRectItem(graphics_view)
        rect
        graphics_view.show()
        #main_widget.show()
        gui.exec()

    def update_gui(self) -> None:
        pass
        
        