from Class163_NexT.models import *
from Class163_NexT.utils import *

# 获取 Cookies
s = selenium_login()
save_cookies(s)
# 导入 Cookies
s = load_cookies()

# 多模态（一）链接
m_url = "https://music.163.com/song?id=1387182799&uct2=U2FsdGVkX18DOaz3Xw7h0bEP2Tl5Lbm0DvOcl3R4ae8="
pl_url = "https://music.163.com/playlist?id=2391850012&uct2=U2FsdGVkX18y65KpHju6/EfnZmrySmf7uEVjbifdti4="
m = Music163(session=s, key_word=m_url).music
pl = Music163(session=s, key_word=pl_url).playlist

# 多模态（二）ID
m_2_url = "1387182799"
pl_2_url = "2391850012"
m_2 = Music163(session=s, key_word=m_url).music
pl_2 = Music163(session=s, key_word=pl_url).playlist

# 多模态（三）搜索音乐/歌单
se_key = "可不"
se = Music163(session=s, key_word=se_key)
m_3 = se.music_search_results
pl_3 = se.playlist_search_results

# Music类操作
m.get_detail(s)                                                     # 获取详细信息
m.get_lyric(s)                                                      # 获取歌词
m.quality = 4                                                       # 修改音质（1~4）
m.get_file(s)                                                       # 获取下载链接
m.download_file(s)                                                  # 下载音乐
m.download_cover(s, pixel=800)                                      # 下载封面
m.metadata_write()                                                  # 写入元数据
m.save("Filename", file=True, cover=True, lyric=True, clean=True)   # 保存

# Playlist类操作
pl.get_info(s)
pl.get_detail(s)
pl.get_lyric(s)
pl.get_file(s)

# 其他提示
pl.tracks[0].metadata_write()

"""
Music 类的定义
class Music:
    def __init__(self,
                 session: EncodeSession,
                 music_id: int,
                 quality: int = 1,
                 detail: bool = False,
                 lyric: bool = False,
                 file: bool = False,
                 detail_pre_dict: dict|None = None,
                 file_pre_dict: dict|None = None):
        # General information
        self.id = music_id
        self.title: str = ""
        self.trans_title: str = ""
        self.subtitle: str = ""
        self.artists: list[str] = []
        self.album: str = ""
        # Cover file
        self.cover_url: str = ""
        self.cover_data: BytesIO = BytesIO()
        # Lyrics
        self.lyric: str = ""
        self.trans_lyric: str = ""
        # Music file
        self.music_url: str = ""
        self.file_data: BytesIO = BytesIO()
        self.quality = quality
"""

"""
Playlist 类的定义
class Playlist:
    def __init__(self,
                 session: EncodeSession,
                 playlist_id: int,
                 quality: int = 1,
                 info: bool = False,
                 detail: bool = False,
                 lyric: bool = False,
                 file: bool = False):
        self.id = playlist_id
        self.title: str = ""
        self.creator: str = ""
        self.create_timestamp: int = -1
        self.last_update_timestamp: int = -1
        self.description: str = ""
        self.track_count: int = -1
        self.tracks: list[Music] = []
"""

"""
Class163 类的定义
class Music163:
    def __init__(self, session: EncodeSession, key_word: str):
        self.session = session
        self.music: Music = Music(session, -1)
        self.playlist: Playlist = Playlist(session, -1)
        self.music_search_results: list[Music] = []
        self.playlist_search_results: list[Playlist] = []
"""