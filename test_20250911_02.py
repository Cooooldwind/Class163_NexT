import time

from Class163_NexT.models.playlist import Playlist
from Class163_NexT.utils import load_cookies

s_2 = load_cookies()
pl2 = Playlist(s_2, 2391850012, 4, False, False,False)

m1 = pl2.tracks[100]
m2 = pl2.tracks[96]

m1.__init__(s_2, m1.id, 3,True, True, True)
m1.download_file()
m1.download_cover(pixel=2000)
m1.metadata_write()
m1.save(f"{m1.title}", True, True, True)

m2.__init__(s_2, m2.id, 4,True, True, True)
m2.download_file()
m2.download_cover(pixel=2000)
m2.metadata_write()
m2.save(f"{m2.title}", True, True, True)
