import os
import time
import requests
import zipfile
from selenium import webdriver
from netease_encode_api import EncodeSession

def download_and_unzip_driver():
    url = "https://msedgedriver.microsoft.com/140.0.3485.54/edgedriver_win64.zip"
    r = requests.get(url, stream=True)
    with open("edgedriver_win64.zip", "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    zip_file = zipfile.ZipFile("edgedriver_win64.zip")
    zip_file.extract("msedgedriver.exe", "Class163_NexT/")
    zip_file.close()
    os.remove("edgedriver_win64.zip")

def cleanup():
    os.remove("Class163_NexT/msedgedriver.exe")

def selenium_login() -> EncodeSession:
    download_and_unzip_driver()
    service = webdriver.EdgeService()
    driver = webdriver.ChromiumEdge(service=service)
    driver.get("https://music.163.com/#/login/")
    driver.refresh()
    while True:
        if driver.get_cookie("MUSIC_U"):
            temp_dict = {}
            for cookie in driver.get_cookies():
                temp_dict.update({cookie["name"]: cookie["value"]})
            session = EncodeSession()
            session.cookies.update(temp_dict)
            driver.quit()
            cleanup()
            return session
        print("Waiting for login...")
        time.sleep(1)
