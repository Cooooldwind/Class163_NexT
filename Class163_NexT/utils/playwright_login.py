import time
import subprocess
import shutil
import os
from playwright.sync_api import sync_playwright
from netease_encode_api import EncodeSession


def ensure_playwright():
    if not shutil.which("playwright"):
        raise RuntimeError("Playwright CLI not found, please run: pip install playwright")
    try:
        subprocess.run(
            ["playwright", "show-browsers"],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        print("No browsers detected, installing Chromium...")
        try:
            subprocess.run(
                ["playwright", "install", "chromium"],
                check=True
            )
        except subprocess.CalledProcessError:
            print("Default download failed, retrying with mirror...")
            env = os.environ.copy()
            env["PLAYWRIGHT_DOWNLOAD_HOST"] = "https://npmmirror.com/mirrors/playwright/"
            subprocess.run(
                ["playwright", "install", "chromium"],
                check=True,
                env=env
            )


def playwright_login() -> EncodeSession:
    ensure_playwright()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://music.163.com/#/login/")
        time.sleep(0.2)
        page.reload()
        print("Waiting for login", end="")
        session = None
        while True:
            cookies = context.cookies()
            cookie_dict = {c["name"]: c["value"] for c in cookies}
            if "MUSIC_U" in cookie_dict:
                session = EncodeSession()
                session.cookies.update(cookie_dict)
                print("OK")
                break
            print(".", end="", flush=True)
            time.sleep(1)
        browser.close()
        return session
