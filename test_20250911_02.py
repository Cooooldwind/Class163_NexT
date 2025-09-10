import time

from Class163_NexT.models.playlist import Playlist
from Class163_NexT.utils import load_cookies

s_2 = load_cookies()
pl2 = Playlist(s_2, 2391850012, 4, False, False,False)
m = pl2.tracks[565]
m.__init__(s_2, m.id, 4,True, True, True)
m.download_file()
m.download_cover(pixel=2000)
m.metadata_write()
m.save(f"{m.title}", True, True, True)
