import requests
import os
import subprocess
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QDateTime

APP_VERSION = '0.4'
VERSION_CHECK_URL = f'https://raw.githubusercontent.com/TraxionRPh/PharmCalc/main/CurrentVersion/CURRENT_VERSION.txt?token={APP_VERSION}'
UPDATE_DOWNLOAD_URL = f'https://raw.githubusercontent.com/TraxionRPh/PharmCalc/main/CurrentVersion/PharmCalcInstaller.exe?token={APP_VERSION}'
UPDATE_DOWNLOAD_DIR = './downloads'
UPDATE_INSTALLER_PATH = os.path.join(UPDATE_DOWNLOAD_DIR, 'PharmCalcInstaller.exe')

class UpdateManager(QObject):
    update_available = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.last_check_timestamp = None
        self.download_thread = None

    def check_for_update(self):
        if self.last_check_timestamp is None or self.is_update_check_needed():
            response = requests.get(VERSION_CHECK_URL)
            if response.status_code == 200:
                latest_version = response.text.strip()
                if latest_version > APP_VERSION:
                    self.update_available.emit(True)
            self.update_available.emit(False)
    
    def is_update_check_needed(self):
        if self.last_check_timestamp is None:
            return True
        current_timestamp = QDateTime.currentDateTime()
        return self.last_check_timestamp.daysTo(current_timestamp) >= 1

    def update_last_check_timestamp(self):
        self.last_check_timestamp = QDateTime.currentDateTime()

    def download_and_apply_update(self):
        if self.download_thread is None or not self.download_thread.isRunning():
            self.download_thread = DownloadThread(UPDATE_DOWNLOAD_URL, UPDATE_DOWNLOAD_DIR)
            self.download_thread.progress.connect(self.update_progress)
            self.download_thread.finished.connect(self.on_download_finished)
            self.download_thread.start()
    
    def update_progress(self, percent):
        if percent >= 100:
            self.apply_update()

    def apply_update(self):
        subprocess.Popen([UPDATE_INSTALLER_PATH, '/SILENT'])

    def on_download_finished(self):
        self.download_thread.deleteLater()
        self.download_thread = None

class DownloadThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self, url, download_dir):
        super().__init__()
        self.url = url
        self.download_dir = download_dir
    
    def run(self):
        response = requests.get(self.url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        bytes_downloaded = 0

        with open(UPDATE_INSTALLER_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    percent = int(bytes_downloaded / total_size * 100)
                    self.progress.emit(percent)
        self.progress.emit(100)