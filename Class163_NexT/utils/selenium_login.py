import os
import time
import requests
import zipfile
import tempfile
from selenium import webdriver
from netease_encode_api import EncodeSession

_DRIVER_TEMP_DIR = ""
_DRIVER_PATH = ""

def download_and_unzip_driver():
    global _DRIVER_TEMP_DIR, _DRIVER_PATH
    _DRIVER_TEMP_DIR = tempfile.mkdtemp(prefix="edgedriver_")
    zip_path = os.path.join(_DRIVER_TEMP_DIR, "edgedriver_win64.zip")
    latest_version = requests.get("https://msedgedriver.microsoft.com/LATEST_STABLE").text.strip()
    url = f"https://msedgedriver.microsoft.com/{latest_version}/edgedriver_win64.zip"
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(zip_path, "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extract("msedgedriver.exe", _DRIVER_TEMP_DIR)
    _DRIVER_PATH = os.path.join(_DRIVER_TEMP_DIR, "msedgedriver.exe")
    os.remove(zip_path)


def cleanup():
    global _DRIVER_TEMP_DIR, _DRIVER_PATH
    os.remove(_DRIVER_PATH)
    os.rmdir(_DRIVER_TEMP_DIR)
    _DRIVER_TEMP_DIR = ""
    _DRIVER_PATH = ""

def selenium_login() -> EncodeSession:
    global _DRIVER_PATH
    download_and_unzip_driver()
    service = webdriver.EdgeService(executable_path=_DRIVER_PATH)
    driver = webdriver.ChromiumEdge(service=service)
    driver.get("https://music.163.com/#/login/")
    time.sleep(0.2)
    driver.refresh()
    while True:
        print("Waiting for login...", end="")
        if driver.get_cookie("MUSIC_U"):
            temp_dict = {}
            for cookie in driver.get_cookies():
                temp_dict.update({cookie["name"]: cookie["value"]})
            session = EncodeSession()
            session.cookies.update(temp_dict)
            print("OK")
            driver.quit()
            cleanup()
            return session
        print()
        time.sleep(1)
