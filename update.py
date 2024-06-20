import requests
import os
import subprocess

APP_VERSION = '1.0.0'
VERSION_CHECK_URL = 'https://raw.githubusercontent.com/TraxionRPh/PharmCalc/main/CurrentVersion/CURRENT_VERSION.txt'
UPDATE_INSTALLER_URL = 'https://raw.githubusercontent.com/TraxionRPh/PharmCalc/main/CurrentVersion/PharmCalcInstaller.exe'
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

def run_installer(installer_path):
    try:
        subprocess.run([installer_path, '/S'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error running installer: {e}')