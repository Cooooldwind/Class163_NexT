"""
Class163_NexT - 网易云音乐下载API库
"""

# 导入主要模块
from .models import Music, Playlist, Class163
from .utils import selenium_login, playwright_login, cookies_manager

__version__ = "0.3.14"
__all__ = [
    "Music", 
    "Playlist", 
    "Class163",
    "selenium_login",
    "playwright_login",
    "cookies_manager"
]