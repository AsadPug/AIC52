from PySide6.QtWidgets import QVBoxLayout, QBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer

from model import GOLEngine

class GUILeft(QVBoxLayout):
    def __init__(self, engine: GOLEngine, timer: QTimer) -> None:
        super().__init__()
        self.engine = engine
        self.timer = timer 

        self.pause_button = QPushButton()
        self.pause_button.setText("Pause")
        self.pause_button.clicked.connect(self.pause)
        self.addWidget(self.pause_button)
    
    def pause(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.setText("Start")
        else:
            self.timer.start()
            self.pause_button.setText("Pause")



class GUIRight(QVBoxLayout):
    def __init__(self, engine: GOLEngine) -> None:
        super().__init__()

        self.engine = engine

        self.addStretch()
        self.stats_alive = QLabel()
        self.stats_dead = QLabel()
        self.stats_alive.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_dead.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        self.addWidget(self.stats_alive)
        self.addWidget(self.stats_dead)

    def update(self) -> None:
        text = f"{self.engine.n_cells_alive} cells alive"
        self.stats_alive.setText(text)
        text = f"{self.engine.n_cells_dead} cells dead"
        self.stats_dead.setText(text)