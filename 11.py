from Class163_NexT.models import Class163
from Class163_NexT.utils.cookies_manager import load_cookies

s = load_cookies()

m = Class163(session=s, key_word="https://music.163.com/song?id=2013714547&uct2=U2FsdGVkX18/BuxzkvkxQCSx6unvzjY4+sPrXPuLYPw=").music
