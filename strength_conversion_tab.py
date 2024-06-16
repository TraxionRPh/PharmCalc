from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QHBoxLayout
from PyQt6.QtGui import QIntValidator

def create_strength_conversion_tab(parent):
    strength_conversion_tab = QWidget()
    layout = QVBoxLayout()

    group_box = QGroupBox()
    group_layout = QVBoxLayout(group_box)

    grid = QGridLayout()
    grid.addWidget(QLabel("ml per dose:"), 0, 0)
    parent.mls_per_dose = QLineEdit()
    parent.mls_per_dose.setValidator(QIntValidator())
    grid.addWidget(parent.mls_per_dose, 0, 1)

    grid.addWidget(QLabel("Total quantity prescribed (ml):"), 1, 0)
    parent.total_quantity_prescribed = QLineEdit()
    parent.total_quantity_prescribed.setValidator(QIntValidator())
    grid.addWidget(parent.total_quantity_prescribed, 1, 1)

    grid.addWidget(QLabel("Current Strength (mg/ml):"), 2, 0)
    parent.current_strength = QComboBox()
    parent.current_strength.addItems(["125 mg/ml", "200 mg/ml", "250 mg/ml", "400 mg/ml", "500 mg/ml"])
    grid.addWidget(parent.current_strength, 2, 1)

    grid.addWidget(QLabel("New Strength (mg/ml):"), 3, 0)
    parent.new_strength = QComboBox()
    parent.new_strength.addItems(["125 mg/ml", "200 mg/ml", "250 mg/ml", "400 mg/ml", "500 mg/ml"])
    grid.addWidget(parent.new_strength, 3, 1)

    button_layout = QHBoxLayout()
    parent.calculate_btn = QPushButton("Convert")
    parent.calculate_btn.clicked.connect(parent.calculate_strength_conversion)
    button_layout.addWidget(parent.calculate_btn)
    button_layout.addStretch()  # Add stretchable space to push result_label to the right
    grid.addLayout(button_layout, 4, 0, 1, 2)

    parent.result_label = QLabel("")
    grid.addWidget(parent.result_label, 5, 0, 1, 2)

    group_layout.addLayout(grid)
    layout.addWidget(group_box)

    strength_conversion_tab.setLayout(layout)
    strength_conversion_tab.setObjectName("Strength Conversion")
    parent.tabs.addTab(strength_conversion_tab, "Strength Conversion")

def calculate_strength_conversion(parent):
    try:
        mls_per_dose = float(parent.mls_per_dose.text())
        total_quantity_prescribed = float(parent.total_quantity_prescribed.text())
        current_strength = float(parent.current_strength.currentText().split()[0])
        new_strength = float(parent.new_strength.currentText().split()[0])

        total_mg = mls_per_dose * current_strength
        new_mls_per_dose = total_mg / new_strength
        new_total_quantity = (total_quantity_prescribed * current_strength) / new_strength

        result_text = f"New ml per dose: {new_mls_per_dose:.2f}\n"
        result_text += f"New total quantity: {new_total_quantity:.2f} ml"
        parent.result_label.setText(result_text)
    except ValueError:
        parent.result_label.setText("Invalid input")
