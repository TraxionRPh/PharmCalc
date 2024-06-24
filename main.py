#pyinstaller --onefile --icon=icon.ico -n PharmCalc --noconsole main.py
import sys
import datetime
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QMessageBox, QProgressDialog
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSettings, Qt
from date_difference_tab import create_date_difference_tab, calculate_date_difference
from fillable_date_tab import create_fillable_tab, calculate_date_addition
from accumulation_calculator_tab import create_accumulation_tab
from dosing_tab import create_dosing_tab, calculate_dosing
from strength_conversion_tab import create_strength_conversion_tab, calculate_strength_conversion
from drop_calculator_tab import create_drop_calculator_tab, calculate_days_supply
from taper_tab import create_taper_tab
from update import check_for_update, download_installer_with_progress, run_installer, APP_VERSION

class PharmacistCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pharmacist Calculator")
        # Uncomment directory based on work station, relative paths dont work for whatever reason
        #self.setWindowIcon(QIcon("C:/GitProjects/PharmCalc/icon.png"))
        self.setWindowIcon(QIcon("C:/Users/Griff/OneDrive/Documents/PythonProjects/PharmCalc/icon.png"))
        self.settings = QSettings("TraxionRPh", "PharmacistCalculator")
        self.load_window_geometry()

        self.run_daily_update()

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.available_tabs = {
            "Date Difference": create_date_difference_tab,
            "Fillable Date": create_fillable_tab,
            "Accumulation Calculator": create_accumulation_tab,
            "Dosing": create_dosing_tab,
            "Strength Conversion": create_strength_conversion_tab,
            "Drops Days Supply Calculator": create_drop_calculator_tab,
            "Taper": create_taper_tab
        }

        self.create_menu_bar()
        self.load_tab_order()
    
    def run_daily_update(self):
        last_update_check_str = self.settings.value("last_update_check")
        last_update_check = datetime.datetime.strptime(last_update_check_str, "%Y-%m-%d") if last_update_check_str else None
        current_date = datetime.datetime.now().date()

        if not last_update_check or last_update_check.date() < current_date:
            self.execute_update_script()
            self.settings.setValue("last_update_check", current_date.strftime("%Y-%m-%d"))

    def execute_update_script(self):
        update_url = check_for_update()
        if update_url:
            reply = QMessageBox.question(self, 'Update Available',
                                        'A new update is available. Do you want to update now?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    progress_dialog_download = QProgressDialog("Downloading update...", "Cancel", 0, 0, self)
                    progress_dialog_download.setWindowModality(Qt.WindowModality.WindowModal)
                    progress_dialog_download.setMinimumDuration(0)
                    progress_dialog_download.setCancelButton(None)
                    progress_dialog_download.setAutoClose(True)

                    installer_path = download_installer_with_progress(update_url, './downloads', progress_dialog_download)
                    #progress_dialog_download.close()
                    if installer_path:

                        progress_dialog_apply = QProgressDialog("Applying update...", "Cancel", 0, 0, self)
                        progress_dialog_apply.setWindowModality(Qt.WindowModality.WindowModal)
                        progress_dialog_apply.setMinimumDuration(0)
                        progress_dialog_apply.setCancelButton(None)
                        progress_dialog_apply.setAutoClose(True)

                        run_installer(installer_path)
                        progress_dialog_apply.close()

                        print("Update applied successfully.")
                        sys.exit(0)
                    else:
                        QMessageBox.critical(self, "Update Error", "Failed to download update.")
                except Exception as e:
                    QMessageBox.critical(self, "Update Error", f"Failed to apply update: {e}")
            else:
                print("Update declined by user.")
        else:
            print("No update available.")

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        view_menu = menu_bar.addMenu("View")
        self.tab_actions = {}
        for tab_name in self.available_tabs.keys():
            action = QAction(tab_name, self, checkable=True)
            action.setChecked(True)
            action.triggered.connect(self.toggle_tab)
            view_menu.addAction(action)
            self.tab_actions[tab_name] = action
        
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        menu_bar.addAction(help_action)

        # Add "About" action directly to the menu bar
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        menu_bar.addAction(about_action)

    def show_help(self):
        help_file = './Help/PharmCalc.chm'
        subprocess.run(['hh.exe', help_file])
    
    def show_about(self):
        about_text = (
            "PharmCalc\n"
            f"Version {APP_VERSION}\n\n"
            "Developed by TraxionRPh"
        )
        QMessageBox.about(self, "About PharmCalc", about_text)
    
    def toggle_tab(self):
        action = self.sender()
        tab_name = action.text()

        if action.isChecked():
            self.available_tabs[tab_name](self)
        else:
            index = self.tabs.indexOf(self.tabs.findChild(QWidget, tab_name))
            if index != -1:
                self.tabs.removeTab(index)
    
    def load_window_geometry(self):
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            self.setGeometry(100, 100, 800, 600)
    
    def save_window_geometry(self):
        self.settings.setValue("geometry", self.saveGeometry())
    
    def load_tab_order(self):
        try:
            tab_order = self.settings.value("tab_order", [], type=list)
            loaded_tabs = set()

            for tab_name in tab_order:
                if tab_name in self.available_tabs:
                    self.available_tabs[tab_name](self)
                    loaded_tabs.add(tab_name)
                    self.tab_actions[tab_name].setChecked(True)
                else:
                    self.tab_actions[tab_name].setChecked(False)
            
            for tab_name, create_function in self.available_tabs.items():
                if tab_name not in loaded_tabs:
                    visible = self.settings.value(f"tab_visible_{tab_name}", True, type=bool)
                    if visible:
                        create_function(self)
                        self.tab_actions[tab_name].setChecked(True)
                    else:
                        self.tab_actions[tab_name].setChecked(False)
        
        except TypeError as e:
            print(f"Error loading tab order: {e}")
            for create_function in self.available_tabs.values():
                create_function(self)

    def save_tab_order(self):
        tab_order = [self.tabs.tabText(i) for i in range(self.tabs.count())]
        self.settings.setValue("tab_order", tab_order)

    def closeEvent(self, event):
        self.save_tab_order()
        self.save_window_geometry()
        for tab_name, action in self.tab_actions.items():
            self.settings.setValue(f"tab_visible_{tab_name}", action.isChecked())
        event.accept()

    def calculate_date_difference(self):
        calculate_date_difference(self)
    
    def calculate_date_addition(self):
        calculate_date_addition(self)

    def calculate_dosing(self):
        calculate_dosing(self)

    def calculate_strength_conversion(self):
        calculate_strength_conversion(self)
    
    def calculate_days_supply(self):
        calculate_days_supply(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PharmacistCalculator()
    window.show()
    sys.exit(app.exec())