from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit, QLineEdit, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator
from datetime import datetime

def create_accumulation_tab(parent):
    accumulation_tab = QWidget()
    layout = QVBoxLayout()

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    container_widget = QWidget()
    parent.grid = QGridLayout(container_widget)
    parent.grid.setSpacing(10)
    parent.grid.setColumnStretch(1, 1)  
    parent.grid.addWidget(QLabel("Fill Date:"), 0, 0, Qt.AlignmentFlag.AlignTop)
    parent.grid.addWidget(QLabel("Days Supply:"), 0, 1, Qt.AlignmentFlag.AlignTop)
    parent.grid.addWidget(QLabel(""), 0, 2)

    parent.fill_dates = []
    parent.days_supply = []
    parent.remove_buttons = []

    container_widget.setLayout(parent.grid)

    scroll_area.setWidget(container_widget)

    layout.addWidget(scroll_area)

    buttons_layout = QGridLayout()

    parent.add_entry_btn = QPushButton("Add Entry")
    parent.add_entry_btn.clicked.connect(lambda: add_entry(parent))
    buttons_layout.addWidget(parent.add_entry_btn, 0, 0)

    parent.calculate_btn = QPushButton("Calculate")
    parent.calculate_btn.clicked.connect(lambda: calculate_accumulation(parent))
    buttons_layout.addWidget(parent.calculate_btn, 0, 1)

    layout.addLayout(buttons_layout)

    parent.accumulation_result = QLabel("")
    layout.addWidget(parent.accumulation_result)

    accumulation_tab.setLayout(layout)
    accumulation_tab.setObjectName("Accumulation Calculator")
    parent.tabs.addTab(accumulation_tab, "Accumulation Calculator")

    add_entry(parent)

    if len(parent.fill_dates) == 1:
        parent.remove_buttons[0].hide()

def add_entry(parent):
    fill_date_edit = QDateEdit(calendarPopup=True)
    fill_date_edit.setDisplayFormat('MM-dd-yyyy')
    fill_date_edit.setDate(QDate.currentDate())
    parent.fill_dates.append(fill_date_edit)

    days_supply_edit = QLineEdit()
    days_supply_edit.setValidator(QIntValidator())
    days_supply_edit.setFixedWidth(100)
    parent.days_supply.append(days_supply_edit)

    remove_btn = QPushButton("x")
    remove_btn.setFixedWidth(30)
    remove_btn.clicked.connect(lambda: remove_entry(parent, fill_date_edit, days_supply_edit, remove_btn))
    parent.remove_buttons.append(remove_btn)

    row = len(parent.fill_dates)
    parent.grid.addWidget(fill_date_edit, row, 0)
    parent.grid.addWidget(days_supply_edit, row, 1)
    parent.grid.addWidget(remove_btn, row, 2)

    if len(parent.fill_dates) == 1:
        remove_btn.setEnabled(False)

def remove_entry(parent, fill_date_edit, days_supply_edit, remove_btn):
    index = parent.fill_dates.index(fill_date_edit)

    if len(parent.fill_dates) > 1:
        parent.fill_dates.pop(index)
        parent.days_supply.pop(index)
        parent.remove_buttons.pop(index)

        parent.grid.removeWidget(fill_date_edit)
        fill_date_edit.deleteLater()

        parent.grid.removeWidget(days_supply_edit)
        days_supply_edit.deleteLater()

        parent.grid.removeWidget(remove_btn)
        remove_btn.deleteLater()

        for i in range(index, len(parent.fill_dates)):
            parent.grid.addWidget(parent.fill_dates[i], i + 1, 0)
            parent.grid.addWidget(parent.days_supply[i], i + 1, 1)
            parent.grid.addWidget(parent.remove_buttons[i], i + 1, 2)

        if len(parent.fill_dates) == 1:
            parent.remove_buttons[0].setEnabled(False)
    else:
        remove_btn.setEnabled(False)

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
