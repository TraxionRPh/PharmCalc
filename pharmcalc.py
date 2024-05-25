import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QDateEdit,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QComboBox,
)
from PyQt6.QtCore import QDate, QSettings
from PyQt6.QtGui import QIntValidator
from datetime import datetime, timedelta

class PharmacistCalculator(QMainWindow):
    #Initialization
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pharmacist Calculator")
        self.setGeometry(100, 100, 800, 600)

        self.settings = QSettings("TraxionRPh", "PharmacistCalculator")
        
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.load_tab_order()

    #Saving and loading
    def load_tab_order(self):
        try:
            tab_order = self.settings.value("tab_order")
            for i in range(len(tab_order)):
                if tab_order[i] == "Date Difference":
                    self.create_date_difference_tab()
                elif tab_order[i] == "Fillable Date":
                    self.create_fillable_tab()
                elif tab_order[i] == "Accumulation Calculator":
                    self.create_accumulation_tab()
                elif tab_order[i] == "Dosing":
                    self.create_dosing_tab()
        except TypeError:
            self.create_date_difference_tab()
            self.create_fillable_tab()
            self.create_accumulation_tab()
            self.create_dosing_tab()

    def save_tab_order(self):
        tab_order = {}
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if tab.objectName() == "Date Difference":
                tab_order[i] = "Date Difference"
            elif tab.objectName() == "Fillable Date":
                tab_order[i] = "Fillable Date"
            elif tab.objectName() == "Accumulation Calculator":
                tab_order[i] = "Accumulation Calculator"
            elif tab.objectName() == "Dosing":
                tab_order[i] = "Dosing"
        self.settings.setValue("tab_order", tab_order)
    
    #Date Difference Tab
    def create_date_difference_tab(self):
        date_difference_tab = QWidget()
        layout = QVBoxLayout()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QLabel("Select date of last fill:"), 0, 0, 1, 2)

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat('MM-dd-yyyy')
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMaximumDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.date_edit.dateChanged.connect(self.calculate_date_difference)
        self.date_edit.setFixedWidth(200)
        grid.addWidget(self.date_edit, 1, 0, 1, 2)

        self.date_diff_result = QLabel("")
        grid.addWidget(self.date_diff_result, 2, 0, 1, 2)

        layout.addLayout(grid)

        date_difference_tab.setLayout(layout)
        date_difference_tab.setObjectName("Date Difference")
        self.tabs.addTab(date_difference_tab, "Date Difference")
    
    def calculate_date_difference(self):
        selected_date = self.date_edit.date().toPyDate()
        today = datetime.today().date()
        diff = (today - selected_date).days
        self.date_diff_result.setText(f"{diff} days ago")

    #Fillable Date Tab
    def create_fillable_tab(self):
        fillable_tab = QWidget()
        layout = QVBoxLayout()
        
        grid_addition = QGridLayout()
        grid_addition.setSpacing(10)
        grid_addition.addWidget(QLabel("Select the fill date:"), 0, 0, 1, 2)

        self.date_add_edit = QDateEdit(calendarPopup=True)
        self.date_add_edit.setDisplayFormat('MM-dd-yyyy')
        self.date_add_edit.setDate(QDate.currentDate())
        self.date_add_edit.setMaximumDate(QDate.currentDate().addDays(365))
        self.date_add_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.date_add_edit.dateChanged.connect(self.calculate_date_addition)
        self.date_add_edit.setFixedWidth(200)
        grid_addition.addWidget(self.date_add_edit, 1, 0, 1, 2)

        grid_addition.addWidget(QLabel("Number of days to add:"), 2, 0)
        self.days_to_add = QLineEdit("0")
        self.days_to_add.setValidator(QIntValidator())
        self.days_to_add.textChanged.connect(self.calculate_date_addition)
        self.days_to_add.setFixedWidth(100)
        grid_addition.addWidget(self.days_to_add, 2, 1)

        self.date_add_result = QLabel("")
        grid_addition.addWidget(self.date_add_result, 3, 0, 1, 2)

        layout.addLayout(grid_addition)

        fillable_tab.setLayout(layout)
        fillable_tab.setObjectName("Fillable Date")
        self.tabs.addTab(fillable_tab, "Fillable Date")

    def calculate_date_addition(self):
        start_date = self.date_add_edit.date().toPyDate()
        try:
            days_str = self.days_to_add.text()
            if days_str:
                days = int(days_str)
            else:
                days = 0
            result_date = start_date + timedelta(days=days)
            self.date_add_result.setText(f"{result_date.strftime('%Y-%m-%d')}")
        except ValueError:
            self.date_add_result.setText("Invalid number of days")
        except OverflowError:
            QMessageBox.critical(self, "Error", "The resulting date is out of range.")
            self.days_to_add.setText("0")
        
    #Accumulation Calculator Tab
    def create_accumulation_tab(self):
        accumulation_tab = QWidget()
        layout = QVBoxLayout()

        self.grid_accumulation = QGridLayout()
        self.grid_accumulation.setSpacing(10)
        self.grid_accumulation.addWidget(QLabel("Fill Date:"), 0, 0)
        self.grid_accumulation.addWidget(QLabel("Days Supply:"), 0, 1)

        self.fill_dates = []
        self.days_supply = []

        self.accumulation_result = QLabel("")
        self.grid_accumulation.addWidget(self.accumulation_result, 4, 0, 1, 3)

        self.add_entry_btn = QPushButton("Add Entry")
        self.add_entry_btn.clicked.connect(self.add_entry)
        self.grid_accumulation.addWidget(self.add_entry_btn, 5, 0, 1, 3)

        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate_accumulation)
        self.grid_accumulation.addWidget(self.calculate_btn, 6, 0, 1, 3)

        layout.addLayout(self.grid_accumulation)

        accumulation_tab.setLayout(layout)
        accumulation_tab.setObjectName("Accumulation Calculator")
        self.tabs.addTab(accumulation_tab, "Accumulation Calculator")

    def add_entry(self):
        fill_date_edit = QDateEdit(calendarPopup=True)
        fill_date_edit.setDisplayFormat('MM-dd-yyyy')
        fill_date_edit.setDate(QDate.currentDate())
        self.fill_dates.append(fill_date_edit)

        days_supply_edit = QLineEdit()
        days_supply_edit.setValidator(QIntValidator())
        days_supply_edit.setFixedWidth(100)
        self.days_supply.append(days_supply_edit)

        row = len(self.fill_dates) + 1
        self.grid_accumulation.addWidget(fill_date_edit, row, 0)
        self.grid_accumulation.addWidget(days_supply_edit, row, 1)

    def calculate_accumulation(self):
        try:
            total_days_supply = 0
            today = datetime.today().date()
            oldest_fill_date = today
            for i in range(len(self.fill_dates)):
                fill_date = self.fill_dates[i].date().toPyDate()
                days_supply = int(self.days_supply[i].text())
                total_days_supply += days_supply
                if fill_date < oldest_fill_date:
                    oldest_fill_date = fill_date
            
            days_since_oldest_fill = (today - oldest_fill_date).days
            days_remaining = total_days_supply - days_since_oldest_fill
            if days_remaining < 0:
                days_remaining = 0
            self.accumulation_result.setText(f"Total accumulated days: {days_remaining}")
        except ValueError:
            self.accumulation_result.setText("Invalid input")

    #Dosing Tab
    def create_dosing_tab(self):
        dosing_tab = QWidget()
        layout = QVBoxLayout()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QLabel("Patient Weight:"), 0, 0)
        self.weight = QLineEdit()
        self.weight.setValidator(QIntValidator())
        self.weight.setFixedWidth(100)
        grid.addWidget(self.weight, 0, 1)

        self.weight_unit = QComboBox()
        self.weight_unit.addItems(["kg", "lbs"])
        self.weight_unit.setFixedWidth(100)
        grid.addWidget(self.weight_unit, 0, 2)

        grid.addWidget(QLabel("Dose (mg):"), 1, 0)
        self.dose = QLineEdit()
        self.dose.setValidator(QIntValidator())
        self.dose.setFixedWidth(100)
        grid.addWidget(self.dose, 1, 1)

        grid.addWidget(QLabel("Dosing Frequency:"), 2, 0)
        self.frequency = QComboBox()
        self.frequency.addItems(["QD", "BID", "TID", "QID"])
        self.frequency.setFixedWidth(100)
        grid.addWidget(self.frequency, 2, 1)

        self.calculate_btn_dosing = QPushButton("Calculate")
        self.calculate_btn_dosing.clicked.connect(self.calculate_dosing)
        grid.addWidget(self.calculate_btn_dosing, 3, 0, 1, 3)

        self.result_label_dosing = QLabel("")
        grid.addWidget(self.result_label_dosing, 4, 0, 1, 3)

        layout.addLayout(grid)

        dosing_tab.setLayout(layout)
        dosing_tab.setObjectName("Dosing")
        self.tabs.addTab(dosing_tab, "Dosing")

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
    
    #Events
    def closeEvent(self, event):
        self.save_tab_order()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PharmacistCalculator()
    window.show()
    sys.exit(app.exec())