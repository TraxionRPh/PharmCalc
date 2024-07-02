from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QHBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QFont, QTextOption

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
        layout.addWidget(scroll_area, stretch=2)

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

        self.taper_result = QTextEdit()
        self.taper_result.setReadOnly(True)  # Make the QTextEdit read-only
        self.taper_result.setWordWrapMode(QTextOption.WrapMode.WordWrap)  # Enable word wrap
        layout.addWidget(self.taper_result, stretch=1)

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
            sig_text = ""

            for i in range(len(self.tablets)):
                days = int(self.days[i].text())
                tablets = float(self.tablets[i].text())
                total_days += days
                total_tablets += tablets * days
                
                if tablets < 1:
                    tablets_str = self.convert_to_fraction(tablets)
                else:
                    tablets_str = str(int(tablets))
                
                if i == 0:
                    sig_text += f"Take {tablets_str} tablet{'s' if tablets > 1 else ''} by mouth once a day for {days} day{'s' if days > 1 else ''}, then "
                else:
                    sig_text += f"take {tablets_str} tablet{'s' if tablets > 1 else ''} daily for {days} day{'s' if days > 1 else ''}, then "

            sig_text = sig_text.rstrip(', then ')
            
            self.taper_result.setHtml(f"Total tablets needed: {total_tablets}<br>How many days it'll last: {total_days}<br>Sample Sig:<br>{sig_text}")
        except ValueError:
            self.taper_result.setHtml("Invalid Input")

    def convert_to_fraction(self, value):
        fractions = {
            0.125: "1/8",
            0.25: "1/4",
            0.375: "3/8",
            0.5: "1/2",
            0.625: "5/8",
            0.75: "3/4",
            0.875: "7/8",
        }
        if value in fractions:
            return fractions[value]
        return str(value)

def create_taper_tab(parent):
    taper_tab = TaperTab(parent)
    taper_tab.setObjectName("Taper")
    parent.tabs.addTab(taper_tab, "Taper")
