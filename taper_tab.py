from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QFont

class TaperTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tablets = []
        self.days = []
        self.remove_buttons = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        labels_layout = QHBoxLayout()
        label_tablets = QLabel("How many tablets")
        label_tablets.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        labels_layout.addWidget(label_tablets)
        label_days = QLabel("How many days")
        label_days.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        labels_layout.addWidget(label_days)
        layout.addLayout(labels_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(QLabel(""), 0, 2)

        container_layout.addLayout(self.grid)
        scroll_area.setWidget(container_widget)
        layout.addWidget(scroll_area)

        buttons_layout = QHBoxLayout()
        self.add_entry_btn = QPushButton("Add Entry")
        self.add_entry_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
        self.add_entry_btn.clicked.connect(self.add_entry)
        buttons_layout.addWidget(self.add_entry_btn)

        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.calculate_btn.clicked.connect(self.calculate_taper)
        buttons_layout.addWidget(self.calculate_btn)
        layout.addLayout(buttons_layout)

        self.taper_result = QLabel("")
        layout.addWidget(self.taper_result)

        self.setLayout(layout)
        self.setObjectName("Taper")
        if self.parent():
            self.parent().tabs.addTab(self, "Taper")

        self.add_entry()

    def add_entry(self):
        tablets_edit = QLineEdit()
        tablets_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        tablets_edit.setValidator(QDoubleValidator(0.0, 1000.0, 2))
        self.tablets.append(tablets_edit)

        days_edit = QLineEdit()
        days_edit.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        days_edit.setValidator(QIntValidator())
        self.days.append(days_edit)

        remove_btn = QPushButton("x")
        remove_btn.setMaximumWidth(30)
        remove_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        remove_btn.setStyleSheet("QPushButton { background-color: #FF5722; color: white; }")
        remove_btn.clicked.connect(lambda: self.remove_entry(tablets_edit, days_edit, remove_btn))
        self.remove_buttons.append(remove_btn)

        row = len(self.tablets) - 1
        self.grid.addWidget(tablets_edit, row, 0, Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(days_edit, row, 1, Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(remove_btn, row, 2)

        if len(self.tablets) == 1:
            remove_btn.hide()

    def remove_entry(self, tablets_edit, days_edit, remove_btn):
        index = self.tablets.index(tablets_edit)

        if len(self.tablets) > 1:
            self.tablets.pop(index)
            self.days.pop(index)
            self.remove_buttons.pop(index)

            self.grid.removeWidget(tablets_edit)
            tablets_edit.deleteLater()

            self.grid.removeWidget(days_edit)
            days_edit.deleteLater()

            self.grid.removeWidget(remove_btn)
            remove_btn.deleteLater()

            for i in range(index, len(self.tablets)):
                self.grid.addWidget(self.tablets[i], i + 1, 0, Qt.AlignmentFlag.AlignTop)
                self.grid.addWidget(self.days[i], i + 1, 1, Qt.AlignmentFlag.AlignTop)
                self.grid.addWidget(self.remove_buttons[i], i + 1, 2)

            if len(self.tablets) == 1:
                self.remove_buttons[0].hide()
        else:
            remove_btn.hide()

    def calculate_taper(self):
        try:
            total_days = 0
            total_tablets = 0

            for i in range(len(self.tablets)):
                days = self.days[i]
                tablets = self.tablets[i]

                total_days += int(days.text())
                total_tablets += float(tablets.text()) * int(days.text())
            
            self.taper_result.setText(f"Total tablets needed: {total_tablets}\nHow many days it'll last: {total_days}")
        except ValueError:
            self.taper_result.setText("Invalid Input")

def create_taper_tab(parent):
    taper_tab = TaperTab(parent)
    taper_tab.setObjectName("Taper")
    parent.tabs.addTab(taper_tab, "Taper")