from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt

class StrengthConversionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
        layout = QVBoxLayout()
        group_box = QGroupBox()
        group_layout = QVBoxLayout(group_box)

        grid = QGridLayout()
        
        label_mls_per_dose = QLabel("ml per dose:")
        label_mls_per_dose.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        grid.addWidget(label_mls_per_dose, 0, 0)
        
        self.mls_per_dose = QLineEdit()
        self.mls_per_dose.setValidator(QIntValidator())
        grid.addWidget(self.mls_per_dose, 0, 1)

        label_total_quantity = QLabel("Total quantity prescribed (ml):")
        label_total_quantity.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        grid.addWidget(label_total_quantity, 1, 0)
        
        self.total_quantity_prescribed = QLineEdit()
        self.total_quantity_prescribed.setValidator(QIntValidator())
        grid.addWidget(self.total_quantity_prescribed, 1, 1)

        label_current_strength = QLabel("Current Strength (mg/ml):")
        label_current_strength.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        grid.addWidget(label_current_strength, 2, 0)
        
        self.current_strength = QComboBox()
        self.current_strength.addItems(["100 mg/ml", "125 mg/ml", "200 mg/ml", "250 mg/ml", "400 mg/ml", "500 mg/ml"])
        grid.addWidget(self.current_strength, 2, 1)

        label_new_strength = QLabel("New Strength (mg/ml):")
        label_new_strength.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        grid.addWidget(label_new_strength, 3, 0)
        
        self.new_strength = QComboBox()
        self.new_strength.addItems(["100 mg/ml", "125 mg/ml", "200 mg/ml", "250 mg/ml", "400 mg/ml", "500 mg/ml"])
        grid.addWidget(self.new_strength, 3, 1)

        button_layout = QHBoxLayout()
        self.calculate_btn = QPushButton("Convert")
        self.calculate_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.calculate_btn.clicked.connect(self.calculate_strength_conversion)
        button_layout.addWidget(self.calculate_btn)
        button_layout.addStretch()  # Add stretchable space to push result_label to the right
        grid.addLayout(button_layout, 4, 0, 1, 2)

        self.result_label = QLabel("")
        grid.addWidget(self.result_label, 5, 0, 1, 2)

        group_layout.addLayout(grid)
        layout.addWidget(group_box)

        self.setLayout(layout)
        self.setObjectName("Strength Conversion")
        parent.tabs.addTab(self, "Strength Conversion")

    def calculate_strength_conversion(self):
        try:
            mls_per_dose = float(self.mls_per_dose.text())
            total_quantity_prescribed = float(self.total_quantity_prescribed.text())
            current_strength = float(self.current_strength.currentText().split()[0])
            new_strength = float(self.new_strength.currentText().split()[0])

            total_mg = mls_per_dose * current_strength
            new_mls_per_dose = total_mg / new_strength
            new_total_quantity = (total_quantity_prescribed * current_strength) / new_strength

            result_text = f"New ml per dose: {new_mls_per_dose:.2f}\n"
            result_text += f"New total quantity: {new_total_quantity:.2f} ml"
            self.result_label.setText(result_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid input")

def create_strength_conversion_tab(parent):
    strength_conversion_tab = StrengthConversionTab(parent)
    strength_conversion_tab.setObjectName("Strength Conversion")
    parent.tabs.addTab(strength_conversion_tab, "Strength Conversion")
