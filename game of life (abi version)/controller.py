import sys 
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer

from model import Grid
from vue import Vue

class MainApplication(QMainWindow):
    def __init__(self, fps: int, width: int, height: int) -> None:
        super().__init__()
        self.window_width = 800    
        self.window_height = 800
        self.setWindowTitle("Pyside graphics view")
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.delay = (1000 / fps)
        self.grid = Grid(width, height)
        self.vue = Vue(self.grid)
        self.timer = QTimer()
        self.timer.timeout.connect(self.new_generation)
        self.timer.start(self.delay)
    
        
    def new_generation(self) -> None:
        self.grid.update_grid()
        self.vue.update_gui()
        

def main():
    app = QApplication(sys.argv)
    main_application = MainApplication(1, 20, 20)
    main_application.show()
    app.exec()

if __name__ == "__main__":
    main()


#https://github.com/semk/GameOfLife/blob/master/gol/gol.py
#game of life pyside ^^^^^^^^