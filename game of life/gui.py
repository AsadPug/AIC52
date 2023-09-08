from PySide6.QtWidgets import QVBoxLayout, QBoxLayout, QLabel, QPushButton, QSlider
from PySide6.QtCore import Qt, QTimer

from model import GOLEngine

class GUILeft(QVBoxLayout):
    def __init__(self, engine: GOLEngine, timer: QTimer) -> None:
        super().__init__()
        self.engine = engine
        self.timer = timer 

        self.fill_percent = 50

        self.pause_button = QPushButton()
        self.fill_slider_label = QLabel()
        self.fill_slider = QSlider()
        self.fill_button = QPushButton()
        
        self.fill_slider.setOrientation(Qt.Orientation.Horizontal)
        self.fill_slider.setMaximum(100)
        self.fill_slider.setMinimum(1)
        self.fill_slider.setSliderPosition(50)
        self.fill_slider.sliderMoved.connect(self.fill_slide)
        self.pause_button.setText("Pause")
        self.fill_slider_label.setText(f"{self.fill_percent} percent alive")
        self.fill_button.setText("Fill grid")
        

        self.pause_button.clicked.connect(self.pause)
        self.fill_button.clicked.connect(self.fill)

        self.addWidget(self.pause_button)
        self.addWidget(self.fill_slider_label)
        self.addWidget(self.fill_slider)
        self.addWidget(self.fill_button)
        self.addStretch()
    
    def pause(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.setText("Start")
        else:
            self.timer.start()
            self.pause_button.setText("Pause")
    
    def fill(self) -> None:
        self.engine.fill_grid(self.fill_percent)
    
    def fill_slide(self) -> None:
        self.fill_percent = self.fill_slider.value()
        self.fill_slider_label.setText(f"{self.fill_percent} percent alive")


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