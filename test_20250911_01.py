import time

from Class163_NexT.models.playlist import Playlist
from Class163_NexT.utils import selenium_login, save_cookies, load_cookies, cookies_exists

if not cookies_exists():
    s_tmp = selenium_login()
    save_cookies(s_tmp)
else:
    s_2 = load_cookies()
    st = time.time()
    pl2 = Playlist(s_2, 2391850012, 3, True, True, True)
    for t in pl2.tracks:
        print(t.title + ": " + str(t.music_url))
    print(time.time() - st)