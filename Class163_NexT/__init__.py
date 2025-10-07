"""
Class163_NexT - 网易云音乐下载API库
"""

# 导入主要模块
from .models import Music, Playlist, Class163
from .utils import safe_run, selenium_login, playwright_login

__version__ = "0.3.11"
__all__ = [
    "Music", 
    "Playlist", 
    "Class163",
    "safe_run",
    "selenium_login",
    "playwright_login"
]