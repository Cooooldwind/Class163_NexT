from Class163_NexT.models.playlist import Playlist
from Class163_NexT.selenium_login import selenium_login

pl = Playlist(selenium_login(), 9097772489, detail=True)
print([t.title for t in pl.tracks])
