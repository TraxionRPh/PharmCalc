from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt

class DosingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(parent)

    def setup_ui(self, parent):
        layout = QVBoxLayout(self)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Patient Weight
        label_weight = QLabel("Patient Weight:")
        label_weight.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        grid.addWidget(label_weight, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.weight = QLineEdit()
        self.weight.setValidator(QIntValidator())
        self.weight.setFixedWidth(100)
        grid.addWidget(self.weight, 0, 1)

        self.weight_unit = QComboBox()
        self.weight_unit.addItems(["kg", "lbs"])
        self.weight_unit.setFixedWidth(100)
        grid.addWidget(self.weight_unit, 0, 2)

        # Dose (mg)
        label_dose = QLabel("Dose (mg):")
        label_dose.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        grid.addWidget(label_dose, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.dose = QLineEdit()
        self.dose.setValidator(QIntValidator())
        self.dose.setFixedWidth(100)
        grid.addWidget(self.dose, 1, 1)

        # Dosing Frequency
        label_frequency = QLabel("Dosing Frequency:")
        label_frequency.setFont(QFont("Arial", weight=QFont.Weight.Bold))
        grid.addWidget(label_frequency, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.frequency = QComboBox()
        self.frequency.addItems(["QD", "BID", "TID", "QID"])
        self.frequency.setFixedWidth(100)
        grid.addWidget(self.frequency, 2, 1)

        # Calculate Button and Result Label
        self.calculate_btn_dosing = QPushButton("Calculate")
        self.calculate_btn_dosing.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.calculate_btn_dosing.clicked.connect(self.calculate_dosing)
        grid.addWidget(self.calculate_btn_dosing, 3, 0, 1, 3)

        self.result_label_dosing = QLabel("")
        grid.addWidget(self.result_label_dosing, 4, 0, 1, 3)

        layout.addLayout(grid)
        self.setObjectName("Dosing")
        parent.tabs.addTab(self, "Dosing")

    def calculate_dosing(self):
        try:
            weight = float(self.weight.text())
            dose = float(self.dose.text())
            
            if self.weight_unit.currentText() == "lbs":
                weight /= 2.2
            
            frequency = self.frequency.currentText()
            doses_per_day = {"QD": 1, "BID": 2, "TID": 3, "QID": 4}[frequency]

            mg_per_kg_per_dose = dose / weight
            mg_per_kg_per_day = mg_per_kg_per_dose * doses_per_day
            total_mg_per_day = dose * doses_per_day

            result_text = f"mg/kg per dose: {mg_per_kg_per_dose:.2f}\n"
            result_text += f"mg/kg per day: {mg_per_kg_per_day:.2f}\n"
            result_text += f"Total mg per day: {total_mg_per_day}"
            self.result_label_dosing.setText(result_text)
        except ValueError:
            self.result_label_dosing.setText("Invalid input")

def create_dosing_tab(parent):
    dosing_tab = DosingTab(parent)
    dosing_tab.setObjectName("Dosing")
    parent.tabs.addTab(dosing_tab, "Dosing")
