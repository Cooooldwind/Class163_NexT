from io import BytesIO
import requests
from netease_encode_api import EncodeSession

DETAIL_URL = "https://music.163.com/weapi/v3/song/detail"
FILE_URL = "https://music.163.com/weapi/song/enhance/player/url/v1"
LYRIC_URL = "https://music.163.com/weapi/song/lyric"
SEARCH_URL = "https://music.163.com/weapi/cloudsearch/get/web"

QUALITY_LIST = ["", "standard", "higher", "exhigh", "lossless"]
QUALITY_FORMAT_LIST = ["", "mp3", "mp3", "mp3", "aac"]

class Music:

    # General information
    id: int = -1
    title: str = ""
    trans_title: str = ""
    subtitle: str = ""
    artists: list[str] = []
    album: str = ""
    # Cover file
    cover_url: str = ""
    cover_data: BytesIO = BytesIO()
    # Lyrics
    lyric: str = ""
    trans_lyric: str = ""
    # Music file
    music_url: str = ""
    music_data: BytesIO = BytesIO()
    quality: int = -1

    # Initialization
    def __init__(self,
                 session: EncodeSession,
                 music_id: int,
                 quality: int = 1,
                 detail: bool = False,
                 lyric: bool = False,
                 file: bool = False):
        """
        初始化一个 Music 类。
        :param session: 带有登录信息的用户会话。
        :param music_id: 音乐 id。
        :param quality: （可选）音乐的音质。默认为标准音质（码率 128kbps 的 MP3 文件，通常 5MB 以内/首。）
        :param detail: （可选）同时获取音乐的详细信息。默认不获取，需要自己执行 get_detail(session) 。
        :param lyric: （可选）同时获取歌词信息（lrc格式）。默认不获取，需要自己执行 get_lyric(session) 。
        :param file: （可选）同时获取音乐文件信息。默认不获取，需要自己执行 get_file(session) 。
        """
        #Write ID & qualify required
        self.id = music_id
        self.quality = quality
        # Get & sort detail information
        if detail: self.get_detail(session)
        # Get & sort lyric information
        if lyric: self.get_lyric(session)
        # Get & sort music file information
        if file: self.get_file(session)

    # Get & sort detail information
    def get_detail(self, session: EncodeSession):
        """
        获取音乐的详细信息，包括：歌曲名称、歌手、专辑等。
        :param session: 带有登录信息的用户会话。
        :return: NULL
        """
        detail_response = session.encoded_post(DETAIL_URL,
                                               {
                                                   "c": str([{"id": str(self.id)}])
                                               }).json()["songs"][0]
        self.title = detail_response["name"]
        self.trans_title = detail_response["tns"][0] \
            if ("tns" in detail_response and len(detail_response["tns"]) > 0) \
            else ""
        self.subtitle = detail_response["alia"][0] \
            if ("alia" in detail_response and len(detail_response["alia"]) > 0) \
            else ""
        self.artists = [artist["name"] for artist in detail_response["ar"]]
        self.album = detail_response["al"]["name"]
        self.cover_url = detail_response["al"]["picUrl"]

    # Get & sort lyric information
    def get_lyric(self, session: EncodeSession):
        """
        获取歌词信息（lrc格式）。
        :param session: 带有登录信息的用户会话。
        :return: NULL
        """
        lyric_response = session.encoded_post(LYRIC_URL,
                                              {
                                                  "id": self.id,
                                                  "lv": -1,
                                                  "tv": -1}).json()
        self.lyric = lyric_response["lrc"]["lyric"]
        self.trans_lyric = lyric_response["tlyric"]["lyric"] \
            if "tlyric" in lyric_response \
            else ""

    # Get & sort music file information
    def get_file(self, session: EncodeSession):
        """
        获取音乐文件信息。
        :param session: 带有登录信息的用户会话。
        :return: NULL
        """
        file_response = session.encoded_post(FILE_URL,
                                             {
                                                 "ids": str([self.id]),
                                                 "level": QUALITY_LIST[self.quality],
                                                 "encodeType": QUALITY_FORMAT_LIST[self.quality]
                                             }).json()["data"][0]
        self.music_url = file_response["url"]

    def download_music(self, filename: str = "NULL"):
        """
        下载音乐。
        :param filename: （可选）文件名。若不填，文件将写入 self.music_data。这是一个 BytesIO 类型的变量。
        :return: NULL
        """
        r = requests.get(self.music_url)
        with open(f"{filename}.{"flac" if self.quality == 4 else "mp3"}", "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    def download_cover(self, filename: str = "NULL", pixel: int = -1):
        """
        下载专辑封面。
        :param filename: （可选）文件名。若不填，文件将写入 self.cover_data。这是一个 BytesIO 类型的变量。
        :param pixel: （可选）图片边长。若不填，图片边长将由网站决定。
        :return: NULL
        """
        r = requests.get(f"{self.cover_url}?param={pixel}y{pixel}" if pixel > 0 else self.cover_url)
        with (self.cover_data if filename == "NULL" else open(f"{filename}.jpg", "wb")) as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)