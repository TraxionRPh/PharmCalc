import requests
import os
import subprocess
import psutil

APP_VERSION = '1.4'
VERSION_CHECK_URL = f'https://raw.githubusercontent.com/TraxionRPh/PharmCalc/main/CurrentVersion/CURRENT_VERSION.txt?token={APP_VERSION}'
UPDATE_INSTALLER_URL = f'https://raw.githubusercontent.com/TraxionRPh/PharmCalc/main/CurrentVersion/PharmCalcInstaller.exe?token={APP_VERSION}'
UPDATE_DOWNLOAD_DIR = './downloads'
INSTALLER_PATH = os.path.join(UPDATE_DOWNLOAD_DIR, 'PharmCalcInstaller.exe')

def check_for_update():
    response = requests.get(VERSION_CHECK_URL)
    if response.status_code == 200:
        latest_version = response.text.strip()
        if latest_version > APP_VERSION:
            return UPDATE_INSTALLER_URL
    return None

def download_installer(url, download_dir):
    response = requests.get(url, stream=True)
    os.makedirs(download_dir, exist_ok=True)
    installer_path = os.path.join(download_dir, 'PharmCalcInstaller.exe')
    with open(installer_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return installer_path

def terminate_processes_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                proc.kill()

def run_installer(installer_path):
    try:
        terminate_processes_by_name('PharmCalc.exe')
        subprocess.Popen([installer_path, '/VERYSILENT', '/NORESTART'])
        os._exit(0)
    except subprocess.CalledProcessError as e:
        print(f'Error running installer: {e}')