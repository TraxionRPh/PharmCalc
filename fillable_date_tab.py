from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit, QLineEdit, QMessageBox, QGroupBox
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QIntValidator, QFont
from datetime import timedelta

class FillableDateTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
        layout = QVBoxLayout()
        group_box = QGroupBox()
        group_layout = QGridLayout()

        label_select_fill_date = QLabel("Select the fill date:")
        label_select_fill_date.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        group_layout.addWidget(label_select_fill_date, 0, 0)
        
        self.date_add_edit = QDateEdit(calendarPopup=True)
        self.date_add_edit.setDisplayFormat('MM-dd-yyyy')
        self.date_add_edit.setDate(QDate.currentDate())
        self.date_add_edit.setMaximumDate(QDate.currentDate().addDays(365))
        self.date_add_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.date_add_edit.dateChanged.connect(self.calculate_date_addition)
        group_layout.addWidget(self.date_add_edit, 0, 1)

        label_days_to_add = QLabel("Number of days to add:")
        label_days_to_add.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        group_layout.addWidget(label_days_to_add, 1, 0)
        
        self.days_to_add = QLineEdit("0")
        self.days_to_add.setValidator(QIntValidator())
        self.days_to_add.textChanged.connect(self.calculate_date_addition)
        group_layout.addWidget(self.days_to_add, 1, 1)

        label_resulting_date = QLabel("Resulting date:")
        label_resulting_date.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        group_layout.addWidget(label_resulting_date, 2, 0)
        
        self.date_add_result = QLabel("")
        group_layout.addWidget(self.date_add_result, 2, 1)

        # Stretch the last row to fill any extra space
        group_layout.setRowStretch(3, 1)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        self.setLayout(layout)
        self.setObjectName("Fillable Date")
        parent.tabs.addTab(self, "Fillable Date")

    def calculate_date_addition(self):
        start_date = self.date_add_edit.date().toPyDate()
        try:
            days_str = self.days_to_add.text()
            if days_str:
                days = int(days_str)
            else:
                days = 0
            result_date = start_date + timedelta(days=days)
            self.date_add_result.setText(f"{result_date.strftime('%m-%d-%Y')}")
        except ValueError:
            self.date_add_result.setText("Invalid number of days")
        except OverflowError:
            QMessageBox.critical(self, "Error", "The resulting date is out of range.")
            self.days_to_add.setText("0")

def create_fillable_tab(parent):
    fillable_tab = FillableDateTab(parent)
    fillable_tab.setObjectName("Fillable Date")
    parent.tabs.addTab(fillable_tab, "Fillable Date")
