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
    cover_file: bytes = b""
    # Lyrics
    lyric: str = ""
    trans_lyric: str = ""
    # Music file
    music_url: str = ""
    music_file: bytes = b""
    quality: int = -1

    # Initialization
    def __init__(self,
                 session: EncodeSession,
                 music_id: int,
                 quality: int = 1,
                 detail: bool = False,
                 lyric: bool = False,
                 file: bool = False):
        #Write ID & qualify required
        self.id = music_id
        self.quality = quality if self.quality != -1 else self.quality
        # Get & sort detail information
        if detail: self.get_detail(session)
        # Get & sort lyric information
        if lyric: self.get_lyric(session)
        # Get & sort music file information
        if file: self.get_file(session)

    # Get & sort detail information
    def get_detail(self, session: EncodeSession):
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
        file_response = session.encoded_post(FILE_URL,
                                             {
                                                 "ids": str([self.id]),
                                                 "level": QUALITY_LIST[self.quality],
                                                 "encodeType": QUALITY_FORMAT_LIST[self.quality]
                                             }).json()["data"][0]
        self.music_url = file_response["url"]

    def download_music(self, filename: str = f"{self.title} - {", ".join(self.artists)}"):
        r = requests.get(self.music_url)
        with open(filename + (".flac" if self.quality > 3 else ".mp3"), "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

