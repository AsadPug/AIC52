import sys 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPalette

from gol_engine import GOLEngine
from gui import TimerControlWidget,GOLMapControlWidget,GOLSizeControlWidget, StatsWidget
from gol_label import GOLLabel


class GOL(QMainWindow):
    def __init__(self, fps: int, width: int, height: int) -> None:
        super().__init__()

        self.setWindowTitle("Game of life")
        self.setGeometry(0,0,800,600)
        self.engine = GOLEngine((width, height))
 
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        self.left_layout = QVBoxLayout()

        self.gol_background = QWidget()
        self.gol_bg_palette = QPalette()
        self.gol_bg_palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.gray)
        self.gol_background.setAutoFillBackground(True)
        self.gol_background.setPalette(self.gol_bg_palette)

        self.gol_layout = QVBoxLayout()

        self.right_layout = QVBoxLayout()
        self.right_layout.addStretch()
        
        self.timer = QTimer()
        
        self.gol_label = GOLLabel(self.engine, self.timer)
        
        
        self.stats_widget = StatsWidget()
        self.timer_control_widget = TimerControlWidget()
        self.map_control_widget = GOLMapControlWidget()
        self.size_control_widget = GOLSizeControlWidget()

        self.right_layout.addWidget(self.stats_widget)
        self.left_layout.addWidget(self.timer_control_widget)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.size_control_widget)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.map_control_widget)
        
        self.main_layout.addLayout(self.left_layout)
        self.gol_background.setLayout(self.gol_layout)
        self.gol_layout.addWidget(self.gol_label)
        self.main_layout.addWidget(self.gol_background)
        self.main_layout.addLayout(self.right_layout)
        
        self.main_layout.setStretchFactor(self.right_layout, 1)
        self.main_layout.setStretchFactor(self.gol_background, 8)
        self.main_layout.setStretchFactor(self.left_layout, 1)

        self.timer.timeout.connect(self.update)
        self.delay = (1000 / fps)
        self.timer.start(self.delay)
        
    def update(self) -> None:
        self.gol_label.update()
        self.stats_widget.set_stats(
            self.engine.n_cells_alive, self.engine.n_cells_dead
        )
        self.engine.tick()
        

    def refresh_view(self) -> None:
        self.engine.tick(False)
        self.gol_label.update()
        self.gol_label.resize()
        self.stats_widget.set_stats(
            self.engine.n_cells_alive, self.engine.n_cells_dead
        )
        

def main():
    app = QApplication(sys.argv)
    gol = GOL(120, 500, 500)
    gol.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


#https://github.com/semk/GameOfLife/blob/master/gol/gol.py
#game of life pyside ^^^^^^^^