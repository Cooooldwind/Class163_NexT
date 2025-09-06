import time
from selenium import webdriver
from netease_encode_api import EncodeSession

def selenium_login() -> EncodeSession:
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
            return session
        print("Waiting for login...")
        time.sleep(1)
