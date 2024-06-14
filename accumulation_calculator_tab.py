from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit, QLineEdit, QPushButton
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator
from datetime import datetime

def create_accumulation_tab(parent):
    accumulation_tab = QWidget()
    layout = QVBoxLayout()

    parent.grid = QGridLayout()
    parent.grid.setSpacing(10)
    parent.grid.addWidget(QLabel("Fill Date:"), 0, 0)
    parent.grid.addWidget(QLabel("Days Supply:"), 0, 1)

    parent.fill_dates = []
    parent.days_supply = []

    parent.accumulation_result = QLabel("")
    parent.grid.addWidget(parent.accumulation_result, 4, 0, 1, 3)

    parent.add_entry_btn = QPushButton("Add Entry")
    parent.add_entry_btn.clicked.connect(parent.add_entry)
    parent.grid.addWidget(parent.add_entry_btn, 5, 0, 1, 3)

    parent.calculate_btn = QPushButton("Calculate")
    parent.calculate_btn.clicked.connect(parent.calculate_accumulation)
    parent.grid.addWidget(parent.calculate_btn, 6, 0, 1, 3)

    layout.addLayout(parent.grid)

    accumulation_tab.setLayout(layout)
    accumulation_tab.setObjectName("Accumulation Calculator")
    parent.tabs.addTab(accumulation_tab, "Accumulation Calculator")

def add_entry(parent):
    fill_date_edit = QDateEdit(calendarPopup=True)
    fill_date_edit.setDisplayFormat('MM-dd-yyyy')
    fill_date_edit.setDate(QDate.currentDate())
    parent.fill_dates.append(fill_date_edit)

    days_supply_edit = QLineEdit()
    days_supply_edit.setValidator(QIntValidator())
    days_supply_edit.setFixedWidth(100)
    parent.days_supply.append(days_supply_edit)

    row = len(parent.fill_dates) + 1
    parent.grid.addWidget(fill_date_edit, row, 0)
    parent.grid.addWidget(days_supply_edit, row, 1)

def calculate_accumulation(parent):
    try:
        total_days_supply = 0
        today = datetime.today().date()
        oldest_fill_date = today
        for i in range(len(parent.fill_dates)):
            fill_date = parent.fill_dates[i].date().toPyDate()
            days_supply = int(parent.days_supply[i].text())
            total_days_supply += days_supply
            if fill_date < oldest_fill_date:
                oldest_fill_date = fill_date

        days_since_oldest_fill = (today - oldest_fill_date).days
        days_remaining = total_days_supply - days_since_oldest_fill
        if days_remaining < 0:
            days_remaining = 0
        parent.accumulation_result.setText(f"Total accumulated days: {days_remaining}")
    except ValueError:
        parent.accumulation_result.setText("Invalid input")
