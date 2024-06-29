from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QMessageBox
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QFont
from PyQt6.QtCore import Qt

class DropCalculatorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
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
            input_layout.addWidget(label, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)  # Align label to the left

            input_field = QLineEdit()
            input_field.setValidator(validator)
            input_field.setMaximumWidth(200)
            input_layout.addWidget(input_field, row, 1, alignment=Qt.AlignmentFlag.AlignLeft)  # Align input field to the left

            return input_field

        self.quantity_edit = add_input_field("Quantity (ml):", QDoubleValidator(0.0, 10000.0, 1), 0)
        self.quantity_edit.setToolTip("Enter the total volume of the solution in milliliters.")

        self.drops_per_dose_edit = add_input_field("Drops per Dose:", QIntValidator(1, 100), 1)
        self.drops_per_dose_edit.setToolTip("Enter the number of drops required per dose.")

        self.doses_per_day_edit = add_input_field("Doses per Day:", QIntValidator(1, 100), 2)
        self.doses_per_day_edit.setToolTip("Enter the number of doses needed per day.")

        site_label = QLabel("Which Eye/Ear:")
        site_label.setFont(label_font)
        site_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        input_layout.addWidget(site_label, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft)  # Align site label to the left

        self.site_combo = QComboBox()
        self.site_combo.addItems(["Right", "Left", "Both"])
        self.site_combo.setMaximumWidth(200)
        input_layout.addWidget(self.site_combo, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)  # Align combo box to the left
        self.site_combo.setToolTip("Select the site of administration.")

        self.calculate_btn = QPushButton("Calculate Days Supply")
        self.calculate_btn.setEnabled(False)
        self.calculate_btn.setMaximumWidth(250)  # Set maximum width for the button
        self.calculate_btn.clicked.connect(lambda: self.calculate_days_supply(parent))
        input_layout.addWidget(self.calculate_btn, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)  # Center align the button

        self.days_supply_result = QLabel("")
        self.days_supply_result.setFont(QFont('Arial', 12))
        input_layout.addWidget(self.days_supply_result, 5, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)  # Center align the result label

        input_group_box.setLayout(input_layout)
        main_layout.addWidget(input_group_box)
        self.setLayout(main_layout)
        self.setObjectName("Drops Days Supply Calculator")
        parent.tabs.addTab(self, "Drops Days Supply Calculator")

        # Connect signals to the slot method
        self.quantity_edit.textChanged.connect(self.validate_inputs)
        self.drops_per_dose_edit.textChanged.connect(self.validate_inputs)
        self.doses_per_day_edit.textChanged.connect(self.validate_inputs)

        self.validate_inputs()  # Initialize button state

    def validate_inputs(self):
        valid = all([
            self.quantity_edit.hasAcceptableInput(),
            self.drops_per_dose_edit.hasAcceptableInput(),
            self.doses_per_day_edit.hasAcceptableInput()
        ])
        self.calculate_btn.setEnabled(valid)

        # Apply stylesheet to make the button look disabled
        if not valid:
            self.calculate_btn.setStyleSheet("background-color: #B3C8E3; color: #a0a0a0;")
        else:
            self.calculate_btn.setStyleSheet("background-color: #2196F3; color: white;")  # Clear stylesheet

    def calculate_days_supply(self, parent):
        try:
            quantity = float(self.quantity_edit.text())
            drops_per_dose = int(self.drops_per_dose_edit.text())
            doses_per_day = int(self.doses_per_day_edit.text())
            site = self.site_combo.currentText()

            multiplier = 1 if site in ["Right", "Left"] else 2

            total_doses = quantity * 20 / drops_per_dose
            days_supply = total_doses / (doses_per_day * multiplier)

            self.days_supply_result.setText(f"Days Supply: {days_supply:.1f} days")
        except ValueError as e:
            QMessageBox.warning(parent, "Input Error", f"Invalid input: {e}")

def create_drop_calculator_tab(parent):
    drop_calculator_tab = DropCalculatorTab(parent)
    drop_calculator_tab.setObjectName("Drops Days Supply Calculator")
    parent.tabs.addTab(drop_calculator_tab, "Drops Days Supply Calculator")
