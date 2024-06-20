import requests
import zipfile
import os

APP_VERSION = '1.0.0'
UPDATE_CHECK_URL = 'http://24.101.0.106:6969/check-update'
UPDATE_DOWNLOAD_DIR = '/update.zip'

def check_for_update():
    response = requests.get(UPDATE_CHECK_URL)
    if response.status_code == 200:
        data = response.json()
        if data['version'] > APP_VERSION:
            return data['url']
    return None

def download_update(url, download_dir):
    response = requests.get(url, stream=True)
    os.makedirs(download_dir, exist_ok=True)
    zip_path = os.path.join(download_dir, 'update.zip')
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
        return zip_path

def apply_update(zip_path, install_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(install_dir)
    os.remove(zip_path)