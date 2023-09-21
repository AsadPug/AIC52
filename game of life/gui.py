import os

from collections.abc import Callable

from PySide6.QtWidgets import (
     QVBoxLayout, QLabel, QPushButton, QSlider, QComboBox, QGroupBox, QWidget
)
from PySide6.QtCore import Qt, QTimer, Signal, Slot

from model import GOLEngine

class TimerControlWidget(QGroupBox):

    pause = Signal()
    changeFps = Signal(int)

    def __init__(self):
        super().__init__()
        self.fps = 30
        
        self.setTitle("Timer Controls")

        self.main_layout = QVBoxLayout()
        self.pause_button = QPushButton()
        self.fps_slider_label = QLabel()
        self.fps_slider = QSlider()
        self.fps_button = QPushButton()

        self.fps_slider.setOrientation(Qt.Orientation.Horizontal)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setSliderPosition(30)
        
        self.pause_button.clicked.connect(self.__emit_pause_signal)
        self.pause_button.clicked.connect(self.__update_pause_button)
        self.fps_slider.actionTriggered.connect(self.__fps_slide)
        self.fps_button.clicked.connect(self.__emit_change_fps_signal)

        self.pause_button.setText("Pause")
        self.fps_slider_label.setText(f"{self.fps} fps")
        self.fps_button.setText("Update fps")

        self.main_layout.addWidget(self.pause_button)
        self.main_layout.addWidget(self.fps_slider_label)
        self.main_layout.addWidget(self.fps_slider)
        self.main_layout.addWidget(self.fps_button)

        self.setLayout(self.main_layout)
    
    @Slot()
    def __emit_pause_signal(self) -> None:
        self.pause.emit()

    @Slot()
    def __emit_change_fps_signal(self) -> None:
        self.changeFps.emit(self.fps)

    @Slot()
    def __update_pause_button(self) -> None:
        if self.pause_button.text() == "Pause":
            self.pause_button.setText("Start")
        else:
            self.pause_button.setText("Pause")
    
    @Slot()
    def __fps_slide(self) -> None:
        self.fps = self.fps_slider.value()
        self.fps_slider_label.setText(f"{self.fps} fps")

class GOLGridControlWidget(QGroupBox):
    fill = Signal(int)
    changeSize = Signal(int, int)
    
    def __init__(self):
        super().__init__()
        
        self.fill_percent = 50

        self.setTitle("Grid Controls")

        self.main_layout = QVBoxLayout()
        self.fill_slider_label = QLabel()
        self.fill_slider = QSlider()
        self.fill_button = QPushButton()
        self.size_picker_label = QLabel()
        self.size_picker = QComboBox()

        self.fill_slider.setOrientation(Qt.Orientation.Horizontal)
        self.fill_slider.setMaximum(100)
        self.fill_slider.setMinimum(1)
        self.fill_slider.setSliderPosition(50)
        self.fill_slider.actionTriggered.connect(self.__fill_slide)

       
        self.fill_slider_label.setText(f"{self.fill_percent} percent alive")
        
        self.fill_button.setText("Fill grid")
        
        self.size_picker_label.setText("Map size select")
        self.populate_size_picker()
        self.size_picker.setCurrentIndex(6)

        self.fill_button.clicked.connect(self.__emit_fill_signal)
        self.fill_slider.valueChanged.connect(self.__fill_slide)
        self.size_picker.currentTextChanged.connect(self.__emit_resize_signal)

        self.main_layout.addWidget(self.fill_slider_label)
        self.main_layout.addWidget(self.fill_slider)
        self.main_layout.addWidget(self.fill_button)
        self.main_layout.addWidget(self.size_picker_label)
        self.main_layout.addWidget(self.size_picker)

        self.setLayout(self.main_layout)

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

    @Slot()
    def __emit_fill_signal(self) -> None:
        self.fill.emit(self.fill_percent)
    
    @Slot()
    def __emit_resize_signal(self) -> None:
        size_str = self.size_picker.currentText().split("x")
        self.changeSize.emit(int(size_str[0]), int(size_str[1]))
    
    @Slot()
    def __fill_slide(self) -> None:
        self.fill_percent = self.fill_slider.value()
        self.fill_slider_label.setText(f"{self.fill_percent} percent alive")

class GOLMapControlWidget(QGroupBox):

    changeMap = Signal(str)

    def __init__(self):
        super().__init__()

        self.setTitle("Map controls")

        self.main_layout = QVBoxLayout()
        self.map_picker_label = QLabel()
        self.map_picker = QComboBox()
        self.map_change_button = QPushButton()

        self.map_picker_label.setText("Premade map select")
        self.populate_map_picker()
        self.map_change_button.setText("Set premade map")

        self.map_change_button.clicked.connect(self.__emit_change_map_signal)

        self.main_layout.addWidget(self.map_picker_label)
        self.main_layout.addWidget(self.map_picker)
        self.main_layout.addWidget(self.map_change_button)

        self.setLayout(self.main_layout)

    def populate_map_picker(self) -> None:
        path = os.path.join(os.path.dirname(__file__), "maps")
        for _, _, file_names in os.walk(path):
            for file_name in file_names:
                self.map_picker.addItem(file_name)

    @Slot()
    def __emit_change_map_signal(self) -> None:
        map = self.map_picker.currentText()
        self.changeMap.emit(map) 
    

class StatsWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Stats")
        self.stats_alive = QLabel()
        self.stats_dead = QLabel()
        self.main_layout = QVBoxLayout()
        self.stats_alive.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_dead.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.stats_alive)
        self.main_layout.addWidget(self.stats_dead) 
        self.setLayout(self.main_layout)

    def set_stats(self, n_cells_alive: int, n_cells_dead: int) -> None:
        text = f"{n_cells_alive} cells alive"
        self.stats_alive.setText(text)
        text = f"{n_cells_dead} cells dead"
        self.stats_dead.setText(text)