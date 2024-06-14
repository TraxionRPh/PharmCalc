from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit
from PyQt6.QtCore import QDate
from datetime import datetime

def create_date_difference_tab(parent):
    date_difference_tab = QWidget()
    layout = QVBoxLayout()

    grid = QGridLayout()
    grid.setSpacing(10)
    grid.addWidget(QLabel("Select date of last fill:"), 0, 0, 1, 2)

    parent.date_edit = QDateEdit(calendarPopup=True)
    parent.date_edit.setDisplayFormat('MM-dd-yyyy')
    parent.date_edit.setDate(QDate.currentDate())
    parent.date_edit.setMaximumDate(QDate.currentDate())
    parent.date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
    parent.date_edit.dateChanged.connect(parent.calculate_date_difference)
    parent.date_edit.setFixedWidth(200)
    grid.addWidget(parent.date_edit, 1, 0, 1, 2)

    parent.date_diff_result = QLabel("")
    grid.addWidget(parent.date_diff_result, 2, 0, 1, 2)

    layout.addLayout(grid)

    date_difference_tab.setLayout(layout)
    date_difference_tab.setObjectName("Date Difference")
    parent.tabs.addTab(date_difference_tab, "Date Difference")

def calculate_date_difference(parent):
    selected_date = parent.date_edit.date().toPyDate()
    today = datetime.today().date()
    diff = (today - selected_date).days
    parent.date_diff_result.setText(f"{diff} days ago")
