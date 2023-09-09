from collections.abc import Callable

from PySide6.QtWidgets import (
     QVBoxLayout, QBoxLayout, QLabel, QPushButton, QSlider, QComboBox
)
from PySide6.QtCore import Qt, QTimer

from model import GOLEngine

class GUILeft(QVBoxLayout):
    def __init__(self, engine: GOLEngine, timer: QTimer, refresh_view: Callable) -> None:
        super().__init__()
        self.engine = engine
        self.timer = timer 

        
        self.refresh_view: Callable = refresh_view

        self.fill_percent = 50
        self.fps = 30

        self.pause_button = QPushButton()
        self.fill_slider_label = QLabel()
        self.fill_slider = QSlider()
        self.fill_button = QPushButton()
        self.fps_slider_label = QLabel()
        self.fps_slider = QSlider()
        self.fps_button = QPushButton()
        self.size_picker_label = QLabel()
        self.size_picker = QComboBox()
        self.map_picker_label = QLabel()
        self.map_picker = QComboBox()
        self.map_change_button = QPushButton()
        
        self.fill_slider.setOrientation(Qt.Orientation.Horizontal)
        self.fill_slider.setMaximum(100)
        self.fill_slider.setMinimum(1)
        self.fill_slider.setSliderPosition(50)
        self.fill_slider.actionTriggered.connect(self.fill_slide)

        self.fps_slider.setOrientation(Qt.Orientation.Horizontal)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setSliderPosition(30)
        self.fps_slider.actionTriggered.connect(self.fps_slide)

        self.pause_button.setText("Pause")
        self.fill_slider_label.setText(f"{self.fill_percent} percent alive")
        self.fps_slider_label.setText(f"{self.fps} fps")
        self.fill_button.setText("Fill grid")
        self.fps_button.setText("Update fps")
        self.size_picker_label.setText("Map size select")
        self.populate_size_picker()
        self.size_picker.setCurrentIndex(6)
        self.map_picker_label.setText("Premade map select")
        self.map_picker.addItem("FlowerOfLife")
        self.map_change_button.clicked.connect(self.change_map)

        self.pause_button.clicked.connect(self.pause)
        self.fill_button.clicked.connect(self.fill)
        self.fps_button.clicked.connect(self.change_fps)
        self.size_picker.currentTextChanged.connect(self.resize)

        self.addWidget(self.pause_button)
        
        self.addWidget(self.fps_slider_label)
        self.addWidget(self.fps_slider)
        self.addWidget(self.fps_button)

        self.addStretch()

        self.addWidget(self.fill_slider_label)
        self.addWidget(self.fill_slider)
        self.addWidget(self.fill_button)
        self.addWidget(self.size_picker_label)
        self.addWidget(self.size_picker)

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
        self.refresh_view()
    
    def fill_slide(self) -> None:
        self.fill_percent = self.fill_slider.value()
        self.fill_slider_label.setText(f"{self.fill_percent} percent alive")
    
    def change_fps(self) -> None:
        self.timer.stop()
        self.timer.start(1000/ self.fps)

    def fps_slide(self) -> None:
        self.fps = self.fps_slider.value()
        self.fps_slider_label.setText(f"{self.fps} fps")

    def resize(self) -> None:
        size = self.size_picker.currentText().split("x")
        self.engine.resize(int(size[0]),int(size[1]))
        self.refresh_view()

    def populate_size_picker(self) -> None:
        options: list[str] = [
            "1000x1000",
            "750x750",
            "500x500",
            "300x300",
            "200x200",
            "150x150",
            "100x100",
            "75x75",
            "50x50",
            "25x25",
            "100x50",
            "50x100"
        ]
        self.size_picker.addItems(options)

    def change_map(self) -> None:
        map = self.map_picker.currentText()
        if map is "flowerOfLife":
            


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