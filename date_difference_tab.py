from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QDateEdit, QGroupBox, QHBoxLayout
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from datetime import datetime

class DateDifferenceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
        layout = QVBoxLayout(self)

        group_box = QGroupBox()
        group_layout = QVBoxLayout()

        # Date selection row
        date_row_layout = QHBoxLayout()
        
        date_label = QLabel("Select date of last fill:")
        date_label.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        date_row_layout.addWidget(date_label)

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat('MM-dd-yyyy')
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMaximumDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.date_edit.dateChanged.connect(self.calculate_date_difference)
        self.date_edit.setFixedWidth(200)
        date_row_layout.addWidget(self.date_edit)

        group_layout.addLayout(date_row_layout)

        # Result row
        self.date_diff_result = QLabel("")
        self.date_diff_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        group_layout.addWidget(self.date_diff_result)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        self.setObjectName("Date Difference")
        parent.tabs.addTab(self, "Date Difference")

    def calculate_date_difference(self):
        selected_date = self.date_edit.date().toPyDate()
        today = datetime.today().date()
        diff = (today - selected_date).days
        self.date_diff_result.setText(f"{diff} days ago")

def create_date_difference_tab(parent):
    date_difference_tab = DateDifferenceTab(parent)
    date_difference_tab.setObjectName("Date Difference")
    parent.tabs.addTab(date_difference_tab, "Date Difference")
