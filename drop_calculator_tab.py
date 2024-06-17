from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt6.QtGui import QIntValidator, QDoubleValidator

def create_drop_calculator_tab(parent):
    drop_calculator_tab = QWidget()
    layout = QVBoxLayout()

    grid = QGridLayout()
    grid.setSpacing(10)
    
    grid.addWidget(QLabel("Quantity (ml):"), 0, 0)
    parent.quantity_edit = QLineEdit()
    parent.quantity_edit.setValidator(QDoubleValidator(0.0, 10000.0, 2))
    grid.addWidget(parent.quantity_edit, 0, 1)

    grid.addWidget(QLabel("Drops per Dose:"), 1, 0)
    parent.drops_per_dose_edit = QLineEdit()
    parent.drops_per_dose_edit.setValidator(QIntValidator(1, 100))
    grid.addWidget(parent.drops_per_dose_edit, 1, 1)

    grid.addWidget(QLabel("Doses per Day:"), 2, 0)
    parent.doses_per_day_edit = QLineEdit()
    parent.doses_per_day_edit.setValidator(QIntValidator(1, 100))
    grid.addWidget(parent.doses_per_day_edit, 2, 1)

    grid.addWidget(QLabel("Which Eye/Ear:"), 3, 0)
    parent.site_combo = QComboBox()
    parent.site_combo.addItems(["Right Eye/Ear", "Left Eye/Ear", "Both Eyes/Ears"])
    grid.addWidget(parent.site_combo, 3, 1)

    parent.calculate_btn = QPushButton("Calculate Days Supply")
    parent.calculate_btn.clicked.connect(lambda: calculate_days_supply(parent))
    grid.addWidget(parent.calculate_btn, 4, 0, 1, 2)

    parent.days_supply_result = QLabel("")
    layout.addWidget(parent.days_supply_result)

    layout.addLayout(grid)
    drop_calculator_tab.setLayout(layout)
    drop_calculator_tab.setObjectName("Drops Days Supply Calculator")
    parent.tabs.addTab(drop_calculator_tab, "Drops Days Supply Calculator")

def calculate_days_supply(parent):
    try:
        quantity = float(parent.quantity_edit.text())
        drops_per_dose = int(parent.drops_per_dose_edit.text())
        doses_per_day = int(parent.doses_per_day_edit.text())
        site = parent.site_combo.currentText()

        multiplier = 1 if site in ["Right Eye/Ear", "Left Eye/Ear"] else 2

        total_doses = quantity * 20 / drops_per_dose
        days_supply = total_doses / (doses_per_day * multiplier)

        parent.days_supply_result.setText(f"Days Supply: {days_supply:.1f} days")
    except ValueError:
        parent.days_supply_result.setText("Invalid input")