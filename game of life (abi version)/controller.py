import sys 
from PySide6.QtWidgets import QApplication

from model import Grid
from vue import Vue

class Controller(QApplication):
    def __init__(self, fps: int, width: int, height: int) -> None:
        super().__init__(sys.argv)
        self.delay = (1/ fps)
        self.grid = Grid(width, height)
        self.vue = Vue()
        self.is_game_over = False

    def start(self) -> None:
        self.loop()
    
    def loop(self) -> None:
        while self.is_game_over is False :
            self.grid.update_grid()
            self.print_grid()
            self.vue.update_gui()
            
            
    #temporary printing
    def print_grid(self) -> None:
        for row in self.grid.cells:
            for case in row:
                print('[]' if case else '  ', end="")
            print("")
        
    
        

def main():
    controller = Controller(2, 20, 20)
    controller.exec()

if __name__ == "__main__":
    main()


#https://github.com/semk/GameOfLife/blob/master/gol/gol.py
#game of life pyside ^^^^^^^^