import sys 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
)
from PySide6.QtCore import QTimer, Qt, Slot
from PySide6.QtGui import QPalette

from gol_engine import GOLEngine
from gui import TimerControlWidget,GOLMapControlWidget,GOLGridControlWidget, StatsWidget
from gol_widget import GOLWidget


class GOL(QMainWindow):
    def __init__(self, fps: int, width: int, height: int) -> None:
        super().__init__()
        self.fps = fps
        self.timer = QTimer()

        self.setWindowTitle("Game of life")
        self.setGeometry(0,0,800,600)
        self.engine = GOLEngine((width, height))
 
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        
        self.gol_widget = GOLWidget(self.engine)

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        
        self.stats_widget = StatsWidget()
        self.timer_control_widget = TimerControlWidget()
        self.map_control_widget = GOLMapControlWidget()
        self.grid_control_widget = GOLGridControlWidget()

        self.right_layout.addStretch()
        self.right_layout.addWidget(self.stats_widget)
        self.left_layout.addWidget(self.timer_control_widget)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.grid_control_widget)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.map_control_widget)
        
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addWidget(self.gol_widget)
        self.main_layout.addLayout(self.right_layout)
        
        self.main_layout.setStretchFactor(self.right_layout, 1)
        self.main_layout.setStretchFactor(self.gol_widget, 8)
        self.main_layout.setStretchFactor(self.left_layout, 1)

        self.timer.timeout.connect(self.update)
        self.timer_control_widget.pause.connect(self.pause)
        self.timer_control_widget.changeFps.connect(self.change_fps)
        self.grid_control_widget.fill.connect(self.fill)
        self.grid_control_widget.changeSize.connect(self.change_size)
        self.map_control_widget.changeMap.connect(self.change_map)
        self.delay = (1000 / fps)
        self.timer.start(self.delay)
        
    def update(self) -> None:
        self.gol_widget.update()
        self.stats_widget.set_stats(
            self.engine.n_cells_alive, self.engine.n_cells_dead
        )
        self.engine.tick()

    def refresh_view(self) -> None:
        self.engine.tick(False)
        self.gol_widget.update()
        self.gol_widget.resize()
        self.stats_widget.set_stats(
            self.engine.n_cells_alive, self.engine.n_cells_dead
        )
        


    @Slot()    
    def pause(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    @Slot()
    def change_fps(self, value: int) -> None:
        self.fps = value
        self.timer.setInterval(1000/ self.fps)

    @Slot()
    def fill(self, value: int) -> None:
        self.engine.fill_grid(value)
        self.refresh_view()
    
    @Slot()
    def change_size(self, width: int, height: int) -> None:
        self.engine.resize(width, height)
        self.refresh_view()

    @Slot()
    def change_map(self, map: str) -> None:
        self.engine.set_map(map)
        self.refresh_view()

    
def main():
    app = QApplication(sys.argv)
    gol = GOL(120, 500, 500)
    gol.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


#https://github.com/semk/GameOfLife/blob/master/gol/gol.py
#game of life pyside ^^^^^^^^