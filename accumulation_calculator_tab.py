from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QHBoxLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator, QFont
from datetime import datetime  # Import datetime module

class AccumulationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fill_dates = []
        self.days_supply = []
        self.remove_buttons = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        labels_layout = QHBoxLayout()
        
        label_fill_date = QLabel("Fill Date")
        label_fill_date.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        labels_layout.addWidget(label_fill_date)
        
        label_days_supply = QLabel("Days Supply")
        label_days_supply.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        labels_layout.addWidget(label_days_supply)
        
        layout.addLayout(labels_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(QLabel(""), 0, 2)  # Empty cell for the "x" button

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
        self.calculate_btn.clicked.connect(self.calculate_accumulation)
        buttons_layout.addWidget(self.calculate_btn)
        layout.addLayout(buttons_layout)

        self.accumulation_result = QLabel("")
        layout.addWidget(self.accumulation_result)

        self.setLayout(layout)
        self.add_entry()

    def add_entry(self):
        fill_date_edit = QDateEdit(calendarPopup=True)
        fill_date_edit.setDisplayFormat('MM-dd-yyyy')
        fill_date_edit.setDate(QDate.currentDate())
        fill_date_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        fill_date_edit.setMinimumWidth(200)
        self.fill_dates.append(fill_date_edit)

        days_supply_edit = QLineEdit()
        days_supply_edit.setValidator(QIntValidator())
        days_supply_edit.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        days_supply_edit.setMinimumWidth(100)
        self.days_supply.append(days_supply_edit)

        remove_btn = QPushButton("x")
        remove_btn.setMaximumWidth(30)
        remove_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        remove_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
        remove_btn.clicked.connect(lambda: self.remove_entry(fill_date_edit, days_supply_edit, remove_btn))
        self.remove_buttons.append(remove_btn)

        row = len(self.fill_dates) - 1
        self.grid.addWidget(fill_date_edit, row, 0, Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(days_supply_edit, row, 1, Qt.AlignmentFlag.AlignTop)
        self.grid.addWidget(remove_btn, row, 2)

        if len(self.fill_dates) == 1:
            remove_btn.hide()

    def remove_entry(self, fill_date_edit, days_supply_edit, remove_btn):
        index = self.fill_dates.index(fill_date_edit)

        if len(self.fill_dates) > 1:
            self.fill_dates.pop(index)
            self.days_supply.pop(index)
            self.remove_buttons.pop(index)

            self.grid.removeWidget(fill_date_edit)
            fill_date_edit.deleteLater()

            self.grid.removeWidget(days_supply_edit)
            days_supply_edit.deleteLater()

            self.grid.removeWidget(remove_btn)
            remove_btn.deleteLater()

            for i in range(index, len(self.fill_dates)):
                self.grid.addWidget(self.fill_dates[i], i + 1, 0, Qt.AlignmentFlag.AlignTop)
                self.grid.addWidget(self.days_supply[i], i + 1, 1, Qt.AlignmentFlag.AlignTop)
                self.grid.addWidget(self.remove_buttons[i], i + 1, 2)

            if len(self.fill_dates) == 1:
                self.remove_buttons[0].hide()
        else:
            remove_btn.hide()

    def calculate_accumulation(self):
        try:
            total_days_supply = 0
            today = datetime.today().date()  # Using datetime module here
            oldest_fill_date = today
            for i in range(len(self.fill_dates)):
                fill_date = self.fill_dates[i].date().toPyDate()
                days_supply = int(self.days_supply[i].text())
                total_days_supply += days_supply
                if fill_date < oldest_fill_date:
                    oldest_fill_date = fill_date

            days_since_oldest_fill = (today - oldest_fill_date).days
            days_remaining = total_days_supply - days_since_oldest_fill
            if days_remaining < 0:
                days_remaining = 0
            self.accumulation_result.setText(f"Total accumulated days: {days_remaining}")
        except ValueError:
            self.accumulation_result.setText("Invalid input")

def create_accumulation_tab(parent):
    accumulation_tab = AccumulationTab(parent)
    accumulation_tab.setObjectName("Accumulation Calculator")
    parent.tabs.addTab(accumulation_tab, "Accumulation Calculator")
