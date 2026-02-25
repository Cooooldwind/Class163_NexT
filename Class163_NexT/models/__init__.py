from netease_encode_api import EncodeSession
from ..utils import safe_run
from .music import Music
from .playlist import Playlist

SEARCH_URL = "https://music.163.com/weapi/cloudsearch/get/web"

class Class163:
    def __init__(self, session: EncodeSession, key_word: str):
        """
        Class163类。这是一个全能类。
        :param session: 用户会话。
        :param key_word: 任何ID/URL/想搜索的词语。
        """
        self.session = session
        self.music: Music = Music(session, 0)
        self.playlist: Playlist = Playlist(session, 0)
        self.music_search_results: list[Music] = []
        self.playlist_search_results: list[Playlist] = []
        # Check playlist / music.
        if key_word.find("music.163.com") >= 0:
            if key_word.find("playlist?id=") >= 0:
                playlist_id = int(key_word[(key_word.find("playlist?id=") + 12):key_word.find("&uct2=")])
                self.playlist = Playlist(session=session, playlist_id=playlist_id)
            elif key_word.find("song?id=") >= 0:
                music_id = int(key_word[(key_word.find("song?id=") + 8):key_word.find("&uct2=")])
                self.music = Music(session=session, music_id=music_id)
        # Search: music result & playlist result
        else:
            try:
                int(key_word)
            # Not URL or ID
            except ValueError: 
                self.search_music(session, str(key_word))
                self.search_playlist(session, str(key_word))
            else:
                self.music = Music(session=session, music_id=int(key_word))
                self.playlist = Playlist(session=session, playlist_id=int(key_word))
        
        

    @safe_run
    def search_music(self, session: EncodeSession, key_word: str):
        data = {
            "s": key_word,
            "type": 1,  # 歌曲-1 专辑-10 歌手-100 歌单-1000
            "offset": "0",
            "total": "true",
            "limit": "100",
        }
        response = session.encoded_post(SEARCH_URL, data).json()["result"]
        count = response["songCount"]
        ret = []
        for i in range(0, count, 100):
            data["offset"] = str(i)
            response = session.encoded_post(SEARCH_URL, data).json()["result"]
            ret += [Music(session, m["id"], detail=True, detail_pre_dict=m) for m in response["songs"]]
        self.music_search_results = ret
        return

    @safe_run
    def search_playlist(self, session: EncodeSession, key_word: str):
        data = {
            "s": key_word,
            "type": 1000,  # 歌曲-1 专辑-10 歌手-100 歌单-1000
            "offset": "0",
            "total": "true",
            "limit": "100",
        }
        response = session.encoded_post(SEARCH_URL, data).json()["result"]
        count = response["playlistCount"]
        ret = []
        for i in range(0, count, 100):
            data["offset"] = str(i)
            response = session.encoded_post(SEARCH_URL, data).json()["result"]
            ret += [Playlist(session, pl["id"], info=True, info_pre_dict=pl) for pl in response["playlists"]]
        self.playlist_search_results = ret
        return
