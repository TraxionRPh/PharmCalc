from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QHBoxLayout
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt

def create_drop_calculator_tab(parent):
    drop_calculator_tab = QWidget()
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(15, 15, 15, 15)

    input_group_box = QGroupBox()
    input_layout = QGridLayout()
    input_layout.setSpacing(10)

    grid = QGridLayout()
    grid.setSpacing(10)
    
    input_layout.addWidget(QLabel("Quantity (ml):"), 0, 0, Qt.AlignmentFlag.AlignRight)
    parent.quantity_edit = QLineEdit()
    parent.quantity_edit.setValidator(QDoubleValidator(0.0, 10000.0, 2))
    input_layout.addWidget(parent.quantity_edit, 0, 1)

    input_layout.addWidget(QLabel("Drops per Dose:"), 1, 0, Qt.AlignmentFlag.AlignRight)
    parent.drops_per_dose_edit = QLineEdit()
    parent.drops_per_dose_edit.setValidator(QIntValidator(1, 100))
    input_layout.addWidget(parent.drops_per_dose_edit, 1, 1)

    input_layout.addWidget(QLabel("Doses per Day:"), 2, 0, Qt.AlignmentFlag.AlignRight)
    parent.doses_per_day_edit = QLineEdit()
    parent.doses_per_day_edit.setValidator(QIntValidator(1, 100))
    input_layout.addWidget(parent.doses_per_day_edit, 2, 1)

    input_layout.addWidget(QLabel("Which Eye/Ear:"), 3, 0, Qt.AlignmentFlag.AlignRight)
    parent.site_combo = QComboBox()
    parent.site_combo.addItems(["Right", "Left", "Both"])
    input_layout.addWidget(parent.site_combo, 3, 1)

    input_group_box.setLayout(input_layout)

    button_layout = QHBoxLayout()
    parent.calculate_btn = QPushButton("Calculate Days Supply")
    parent.calculate_btn.clicked.connect(lambda: calculate_days_supply(parent))
    button_layout.addWidget(parent.calculate_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    parent.days_supply_result = QLabel("")
    parent.days_supply_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
    button_layout.addWidget(parent.days_supply_result)

    main_layout.addWidget(input_group_box)
    main_layout.addLayout(button_layout)

    drop_calculator_tab.setLayout(main_layout)
    drop_calculator_tab.setObjectName("Drops Days Supply Calculator")
    parent.tabs.addTab(drop_calculator_tab, "Drops Days Supply Calculator")

def calculate_days_supply(parent):
    try:
        quantity = float(parent.quantity_edit.text())
        drops_per_dose = int(parent.drops_per_dose_edit.text())
        doses_per_day = int(parent.doses_per_day_edit.text())
        site = parent.site_combo.currentText()

        multiplier = 1 if site in ["Right", "Left"] else 2

        total_doses = quantity * 20 / drops_per_dose
        days_supply = total_doses / (doses_per_day * multiplier)

        parent.days_supply_result.setText(f"Days Supply: {days_supply:.1f} days")
    except ValueError:
        parent.days_supply_result.setText("Invalid input")