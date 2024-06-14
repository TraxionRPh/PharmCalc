from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit, QLineEdit, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator
from datetime import timedelta

def create_fillable_tab(parent):
    fillable_tab = QWidget()
    layout = QVBoxLayout()

    grid_addition = QGridLayout()
    grid_addition.setSpacing(10)
    grid_addition.addWidget(QLabel("Select the fill date:"), 0, 0, 1, 2)

    parent.date_add_edit = QDateEdit(calendarPopup=True)
    parent.date_add_edit.setDisplayFormat('MM-dd-yyyy')
    parent.date_add_edit.setDate(QDate.currentDate())
    parent.date_add_edit.setMaximumDate(QDate.currentDate().addDays(365))
    parent.date_add_edit.setMinimumDate(QDate.currentDate().addDays(-365))
    parent.date_add_edit.dateChanged.connect(parent.calculate_date_addition)
    parent.date_add_edit.setFixedWidth(200)
    grid_addition.addWidget(parent.date_add_edit, 1, 0, 1, 2)

    grid_addition.addWidget(QLabel("Number of days to add:"), 2, 0)
    parent.days_to_add = QLineEdit("0")
    parent.days_to_add.setValidator(QIntValidator())
    parent.days_to_add.textChanged.connect(parent.calculate_date_addition)
    parent.days_to_add.setFixedWidth(100)
    grid_addition.addWidget(parent.days_to_add, 2, 1)

    parent.date_add_result = QLabel("")
    grid_addition.addWidget(parent.date_add_result, 3, 0, 1, 2)

    layout.addLayout(grid_addition)

    fillable_tab.setLayout(layout)
    fillable_tab.setObjectName("Fillable Date")
    parent.tabs.addTab(fillable_tab, "Fillable Date")

def calculate_date_addition(parent):
    start_date = parent.date_add_edit.date().toPyDate()
    try:
        days_str = parent.days_to_add.text()
        if days_str:
            days = int(days_str)
        else:
            days = 0
        result_date = start_date + timedelta(days=days)
        parent.date_add_result.setText(f"{result_date.strftime('%Y-%m-%d')}")
    except ValueError:
        parent.date_add_result.setText("Invalid number of days")
    except OverflowError:
        QMessageBox.critical(parent, "Error", "The resulting date is out of range.")
        parent.days_to_add.setText("0")
