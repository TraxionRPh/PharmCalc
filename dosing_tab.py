from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt6.QtGui import QIntValidator

def create_dosing_tab(parent):
    dosing_tab = QWidget()
    layout = QVBoxLayout()

    grid = QGridLayout()
    grid.setSpacing(10)
    grid.addWidget(QLabel("Patient Weight:"), 0, 0)
    parent.weight = QLineEdit()
    parent.weight.setValidator(QIntValidator())
    parent.weight.setFixedWidth(100)
    grid.addWidget(parent.weight, 0, 1)

    parent.weight_unit = QComboBox()
    parent.weight_unit.addItems(["kg", "lbs"])
    parent.weight_unit.setFixedWidth(100)
    grid.addWidget(parent.weight_unit, 0, 2)

    grid.addWidget(QLabel("Dose (mg):"), 1, 0)
    parent.dose = QLineEdit()
    parent.dose.setValidator(QIntValidator())
    parent.dose.setFixedWidth(100)
    grid.addWidget(parent.dose, 1, 1)

    grid.addWidget(QLabel("Dosing Frequency:"), 2, 0)
    parent.frequency = QComboBox()
    parent.frequency.addItems(["QD", "BID", "TID", "QID"])
    parent.frequency.setFixedWidth(100)
    grid.addWidget(parent.frequency, 2, 1)

    parent.calculate_btn_dosing = QPushButton("Calculate")
    parent.calculate_btn_dosing.clicked.connect(parent.calculate_dosing)
    grid.addWidget(parent.calculate_btn_dosing, 3, 0, 1, 3)

    parent.result_label_dosing = QLabel("")
    grid.addWidget(parent.result_label_dosing, 4, 0, 1, 3)

    layout.addLayout(grid)

    dosing_tab.setLayout(layout)
    dosing_tab.setObjectName("Dosing")
    parent.tabs.addTab(dosing_tab, "Dosing")

def calculate_dosing(parent):
    try:
        weight = float(parent.weight.text())
        dose = float(parent.dose.text())
        if parent.weight_unit.currentText() == "lbs":
            weight /= 2.2

        frequency = parent.frequency.currentText()
        doses_per_day = {"QD": 1, "BID": 2, "TID": 3, "QID": 4}[frequency]

        mg_per_kg_per_dose = dose / weight
        mg_per_kg_per_day = mg_per_kg_per_dose * doses_per_day
        total_mg_per_day = dose * doses_per_day

        result_text = f"mg/kg per dose: {mg_per_kg_per_dose:.2f}\n"
        result_text += f"mg/kg per day: {mg_per_kg_per_day:.2f}\n"
        result_text += f"Total mg per day: {total_mg_per_day}"
        parent.result_label_dosing.setText(result_text)
    except ValueError:
        parent.result_label_dosing.setText("Invalid input")
