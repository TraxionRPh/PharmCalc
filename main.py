import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import QSettings
from date_difference_tab import create_date_difference_tab, calculate_date_difference
from fillable_date_tab import create_fillable_tab, calculate_date_addition
from accumulation_calculator_tab import create_accumulation_tab, add_entry, calculate_accumulation
from dosing_tab import create_dosing_tab, calculate_dosing
from strength_conversion_tab import create_strength_conversion_tab, calculate_strength_conversion

class PharmacistCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pharmacist Calculator")
        self.setGeometry(100, 100, 800, 600)

        self.settings = QSettings("TraxionRPh", "PharmacistCalculator")

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.load_tab_order()
        self.apply_stylesheet()

    def load_tab_order(self):
        try:
            tab_order = self.settings.value("tab_order")
            for tab_name in tab_order:
                if tab_name == "Date Difference":
                    create_date_difference_tab(self)
                elif tab_name == "Fillable Date":
                    create_fillable_tab(self)
                elif tab_name == "Accumulation Calculator":
                    create_accumulation_tab(self)
                elif tab_name == "Dosing":
                    create_dosing_tab(self)
                elif tab_name == "Strength Conversion":
                    create_strength_conversion_tab(self)
        except TypeError:
            create_date_difference_tab(self)
            create_fillable_tab(self)
            create_accumulation_tab(self)
            create_dosing_tab(self)
            create_strength_conversion_tab(self)

    def save_tab_order(self):
        tab_order = [self.tabs.tabText(i) for i in range(self.tabs.count())]
        self.settings.setValue("tab_order", tab_order)
    
    def apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
            }
            QDateEdit {
                font-size: 14px;
            }
            QComboBox {
                font-size: 14px;
            }
            QPushButton {
                font-size: 14px;
            }
        """)

    def closeEvent(self, event):
        self.save_tab_order()
        event.accept()

    def calculate_date_difference(self):
        calculate_date_difference(self)
    
    def calculate_date_addition(self):
        calculate_date_addition(self)

    def add_entry(self):
        add_entry(self)

    def calculate_accumulation(self):
        calculate_accumulation(self)

    def calculate_dosing(self):
        calculate_dosing(self)

    def calculate_strength_conversion(self):
        calculate_strength_conversion(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PharmacistCalculator()
    window.show()
    sys.exit(app.exec())
