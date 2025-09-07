from Class163_NexT.models.music import Music
from Class163_NexT.selenium_login import selenium_login

session = selenium_login()
music = Music(session=session, music_id=2621539078, quality=4, detail=True, lyric=True, file=True)
print(music.music_url)
music.download_music()