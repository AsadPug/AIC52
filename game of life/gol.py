import sys 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSizePolicy, QHBoxLayout, QVBoxLayout,
    QWidget
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPalette

from model import GOLEngine
from gui import GUILeft, GUIRight
from gol_label import GOLLabel


class GOL(QMainWindow):
    def __init__(self, fps: int, width: int, height: int) -> None:
        super().__init__()

        self.setWindowTitle("Game of life")
        self.setGeometry(0,0,800,600)
        self.engine = GOLEngine(width, height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.gol_background = QWidget()
        self.gol_bg_palette = QPalette()
        self.gol_bg_palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.gray)
        self.gol_background.setAutoFillBackground(True)
        self.gol_background.setPalette(self.gol_bg_palette)
        self.gol_layout = QVBoxLayout()
        
        self.timer = QTimer()
        
        
        self.gol_label = GOLLabel(self.engine)
        self.gui_right = GUIRight(self.engine)
        self.gui_left = GUILeft(self.engine, self.timer)

        self.main_layout.addLayout(self.gui_left)
        self.gol_background.setLayout(self.gol_layout)
        self.gol_layout.addWidget(self.gol_label)
        self.main_layout.addWidget(self.gol_background)
        self.main_layout.addLayout(self.gui_right)
        

        
        self.main_layout.setStretchFactor(self.gui_right, 1)
        self.main_layout.setStretchFactor(self.gol_background, 8)
        self.main_layout.setStretchFactor(self.gui_left, 1)
    
        
        
        self.timer.timeout.connect(self.update)
        self.delay = (1000 / fps)
        self.timer.start(self.delay)
        
    def update(self) -> None:
        self.gol_label.update()
        self.gui_right.update()
        self.engine.update_grid()
        
        
    

    

def main():
    app = QApplication(sys.argv)
    gol = GOL(30, 70, 70)
    gol.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


#https://github.com/semk/GameOfLife/blob/master/gol/gol.py
#game of life pyside ^^^^^^^^