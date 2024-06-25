from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QFont
from PyQt6.QtCore import Qt

def create_drop_calculator_tab(parent):
    drop_calculator_tab = QWidget()
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(15, 15, 15, 15)
    main_layout.setSpacing(20)

    input_group_box = QGroupBox("Input Parameters")
    input_layout = QGridLayout()
    input_layout.setSpacing(10)

    label_font = QFont()
    label_font.setPointSize(10)
    label_font.setBold(True)

    def add_input_field(label_text, validator, row):
        label = QLabel(label_text)
        label.setFont(label_font)
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        input_layout.addWidget(label, row, 0)
        
        input_field = QLineEdit()
        input_field.setValidator(validator)
        input_field.setMaximumWidth(200)
        input_layout.addWidget(input_field, row, 1)
        
        return input_field

    parent.quantity_edit = add_input_field("Quantity (ml):", QDoubleValidator(0.0, 10000.0, 1), 0)
    parent.quantity_edit.setToolTip("Enter the total volume of the solution in milliliters.")

    parent.drops_per_dose_edit = add_input_field("Drops per Dose:", QIntValidator(1, 100), 1)
    parent.drops_per_dose_edit.setToolTip("Enter the number of drops required per dose.")

    parent.doses_per_day_edit = add_input_field("Doses per Day:", QIntValidator(1, 100), 2)
    parent.doses_per_day_edit.setToolTip("Enter the number of doses needed per day.")

    site_label = QLabel("Which Eye/Ear:")
    site_label.setFont(label_font)
    site_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    input_layout.addWidget(site_label, 3, 0)

    parent.site_combo = QComboBox()
    parent.site_combo.addItems(["Right", "Left", "Both"])
    parent.site_combo.setMaximumWidth(200)
    input_layout.addWidget(parent.site_combo, 3, 1)
    parent.site_combo.setToolTip("Select the site of administration.")

    parent.calculate_btn = QPushButton("Calculate Days Supply")
    parent.calculate_btn.setEnabled(False)
    parent.calculate_btn.clicked.connect(lambda: calculate_days_supply(parent))
    input_layout.addWidget(parent.calculate_btn, 4, 0, 1, 2)

    parent.days_supply_result = QLabel("")
    parent.days_supply_result.setFont(QFont('Arial', 12))
    input_layout.addWidget(parent.days_supply_result, 5, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

    input_group_box.setLayout(input_layout)
    main_layout.addWidget(input_group_box)
    drop_calculator_tab.setLayout(main_layout)
    drop_calculator_tab.setObjectName("Drops Days Supply Calculator")
    parent.tabs.addTab(drop_calculator_tab, "Drops Days Supply Calculator")

    for field in [parent.quantity_edit, parent.drops_per_dose_edit, parent.doses_per_day_edit]:
        field.textChanged.connect(lambda: validate_inputs(parent))

def validate_inputs(parent):
    valid = all([parent.quantity_edit.hasAcceptableInput(),
                parent.drops_per_dose_edit.hasAcceptableInput(),
                parent.doses_per_day_edit.hasAcceptableInput()])
    parent.calculate_btn.setEnabled(valid)

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
    except ValueError as e:
        QMessageBox.warning(parent, "Input Error", f"Invalid input: {e}")
