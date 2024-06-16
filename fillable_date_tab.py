from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit, QLineEdit, QMessageBox, QGroupBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator
from datetime import timedelta

def create_fillable_tab(parent):
    fillable_tab = QWidget()
    layout = QVBoxLayout()

    group_box = QGroupBox()
    group_layout = QGridLayout()

    group_layout.addWidget(QLabel("Select the fill date:"), 0, 0)
    parent.date_add_edit = QDateEdit(calendarPopup=True)
    parent.date_add_edit.setDisplayFormat('MM-dd-yyyy')
    parent.date_add_edit.setDate(QDate.currentDate())
    parent.date_add_edit.setMaximumDate(QDate.currentDate().addDays(365))
    parent.date_add_edit.setMinimumDate(QDate.currentDate().addDays(-365))
    parent.date_add_edit.dateChanged.connect(parent.calculate_date_addition)
    group_layout.addWidget(parent.date_add_edit, 0, 1)

    group_layout.addWidget(QLabel("Number of days to add:"), 1, 0)
    parent.days_to_add = QLineEdit("0")
    parent.days_to_add.setValidator(QIntValidator())
    parent.days_to_add.textChanged.connect(parent.calculate_date_addition)
    group_layout.addWidget(parent.days_to_add, 1, 1)

    # Resulting date label aligned with the input fields
    group_layout.addWidget(QLabel("Resulting date:"), 2, 0)
    parent.date_add_result = QLabel("")
    group_layout.addWidget(parent.date_add_result, 2, 1)

    # Stretch the last row to fill any extra space
    group_layout.setRowStretch(3, 1)

    group_box.setLayout(group_layout)
    layout.addWidget(group_box)

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
