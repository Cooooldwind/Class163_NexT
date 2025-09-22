from Class163_NexT.utils.playwright_login import playwright_login
from Class163_NexT.models.playlist import Playlist

s = playwright_login()
p = Playlist(s, 2391850012, True, True)
for i in p.tracks: print(i.title)
