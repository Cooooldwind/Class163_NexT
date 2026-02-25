import concurrent.futures
from ..utils import safe_run
from netease_encode_api import EncodeSession
from Class163_NexT.models.music import Music

PLAYLIST_URL = "https://music.163.com/weapi/v6/playlist/detail"
DETAIL_URL = "https://music.163.com/weapi/v3/song/detail"
FILE_URL = "https://music.163.com/weapi/song/enhance/player/url/v1"

QUALITY_LIST = ["", "standard", "higher", "exhigh", "lossless"]
QUALITY_FORMAT_LIST = ["", "mp3", "mp3", "mp3", "aac"]

@safe_run
def retail_get_tracks_detail(session: EncodeSession, tracks: list[Music]) -> list[Music]:
    detail_response = session.encoded_post(DETAIL_URL,
                                           {
                                               "c": str([{"id": str(track.id)} for track in tracks]),
                                           }).json()["songs"]
    ret: list[Music] = tracks
    for index, track in enumerate(ret): track.get_detail(EncodeSession(), detail_response[index])
    return ret

@safe_run
def retail_get_tracks_file(session: EncodeSession, tracks: list[Music], quality: int = 1) -> list[Music]:
    file_response = session.encoded_post(FILE_URL,
                                           {
                                               "ids": str([str(track.id) for track in tracks]),
                                               "level": QUALITY_LIST[quality],
                                               "encodeType": QUALITY_FORMAT_LIST[quality]
                                           })
    file_response = file_response.json()["data"]
    ret: list[Music] = tracks
    for index, track in enumerate(ret): track.get_file(EncodeSession(), file_response[index])
    return ret

@safe_run
def retail_get(session: EncodeSession, tracks: list[Music],
               quality: int = 1,
               detail: bool = False,
               file: bool = False,
               ) -> list[Music]:
    ret: list[Music] = tracks
    if detail: ret = retail_get_tracks_detail(session, ret)
    if file: ret = retail_get_tracks_file(session, ret, quality)
    return ret

class Playlist:

    @safe_run
    def __init__(self,
                 session: EncodeSession,
                 playlist_id: int,
                 quality: int = 1,
                 info: bool = False,
                 detail: bool = False,
                 lyric: bool = False,
                 file: bool = False,
                 info_pre_dict: dict|None = None):
        if playlist_id < 0: return
        # Write ID
        self.id = playlist_id
        self.title: str = ""
        self.creator: str = ""
        self.create_timestamp: int = -1
        self.last_update_timestamp: int = -1
        self.description: str = ""
        self.track_count: int = -1
        self.tracks: list[Music] = []
        # Get & sort playlist information
        if info: self.get_info(session, info_pre_dict if info_pre_dict else None)
        # Deal with tracks in concurrent.futures. Optimized in 0.1.3. Didn't test.
        if detail: self.get_detail(session)
        if lyric: self.get_lyric(session)
        if file: self.get_file(session)

    @safe_run
    def get_info(self, session: EncodeSession, pre_dict: dict|None = None):
        playlist_response = session.encoded_post(PLAYLIST_URL, {"id": self.id}).json()["playlist"] \
                            if pre_dict is None else pre_dict
        self.title = playlist_response["name"]
        self.creator = playlist_response["creator"]["nickname"]
        self.create_timestamp = playlist_response["createTime"] if "createTime" in playlist_response else -1
        self.last_update_timestamp = playlist_response["updateTime"] if "updateTime" in playlist_response else -1
        self.description = playlist_response["description"]
        self.track_count = playlist_response["trackCount"]
        self.tracks = [Music(EncodeSession(), track["id"]) for track in playlist_response["trackIds"]] if "trackIds" in playlist_response else []

    @safe_run
    def get_detail(self, session: EncodeSession):
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            per_sum = 10 ** (len(str(self.track_count)) - 1)
            for i in range(0, self.track_count, per_sum):
                futures.append(executor.submit(retail_get_tracks_detail,
                                               session,
                                               self.tracks[i:i + per_sum]))
            self.tracks = [t for f in futures for t in f.result()]

    @safe_run
    def get_file(self, session: EncodeSession, quality: int = 1):
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            per_sum = 10 ** (len(str(self.track_count)) - 1)
            for i in range(0, self.track_count, per_sum):
                futures.append(executor.submit(retail_get_tracks_file,
                                               session,
                                               self.tracks[i:i + per_sum],
                                               quality))
            self.tracks = [t for f in futures for t in f.result()]

    @safe_run
    def get_lyric(self, session: EncodeSession):
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in self.tracks:
                futures.append(executor.submit(i.get_lyric, session))