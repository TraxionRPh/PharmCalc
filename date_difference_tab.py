from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDateEdit, QGroupBox, QHBoxLayout
from PyQt6.QtCore import QDate, Qt
from datetime import datetime

def create_date_difference_tab(parent):
    date_difference_tab = QWidget()
    layout = QVBoxLayout()

    group_box = QGroupBox()
    group_layout = QVBoxLayout()

    # Date selection row
    date_row_layout = QHBoxLayout()
    date_label = QLabel("Select date of last fill:")
    date_row_layout.addWidget(date_label)

    parent.date_edit = QDateEdit(calendarPopup=True)
    parent.date_edit.setDisplayFormat('MM-dd-yyyy')
    parent.date_edit.setDate(QDate.currentDate())
    parent.date_edit.setMaximumDate(QDate.currentDate())
    parent.date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
    parent.date_edit.dateChanged.connect(parent.calculate_date_difference)
    parent.date_edit.setFixedWidth(200)
    date_row_layout.addWidget(parent.date_edit)

    group_layout.addLayout(date_row_layout)

    # Result row
    parent.date_diff_result = QLabel("")
    parent.date_diff_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
    group_layout.addWidget(parent.date_diff_result)

    group_box.setLayout(group_layout)
    layout.addWidget(group_box)

    date_difference_tab.setLayout(layout)
    date_difference_tab.setObjectName("Date Difference")
    parent.tabs.addTab(date_difference_tab, "Date Difference")

def calculate_date_difference(parent):
    selected_date = parent.date_edit.date().toPyDate()
    today = datetime.today().date()
    diff = (today - selected_date).days
    parent.date_diff_result.setText(f"{diff} days ago")
