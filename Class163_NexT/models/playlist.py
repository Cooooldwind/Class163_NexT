import concurrent.futures
from netease_encode_api import EncodeSession
from .music import Music

PLAYLIST_URL = "https://music.163.com/weapi/v6/playlist/detail"
DETAIL_URL = "https://music.163.com/weapi/v3/song/detail"
FILE_URL = "https://music.163.com/weapi/song/enhance/player/url/v1"

QUALITY_LIST = ["", "standard", "higher", "exhigh", "lossless"]
QUALITY_FORMAT_LIST = ["", "mp3", "mp3", "mp3", "aac"]

def retail_get_tracks_detail(session: EncodeSession, tracks: list[Music]) -> list[Music]:
    detail_response = session.encoded_post(DETAIL_URL,
                                           {
                                               "c": str([{"id": str(track.id)} for track in tracks]),
                                           }).json()["songs"]
    ret: list[Music] = tracks
    for index, track in enumerate(ret): track.get_detail(EncodeSession(), detail_response[index])
    return ret

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
    id: int = -1
    title: str = ""
    creator: str = ""
    create_timestamp: int = -1
    last_update_timestamp: int = -1
    description: str = ""
    track_count: int = -1
    tracks: list[Music] = []

    def __init__(self,
                 session: EncodeSession,
                 playlist_id: int,
                 quality: int = 1,
                 detail: bool = False,
                 lyric: bool = False,
                 file: bool = False):
        # Write ID
        self.id = playlist_id
        # Get & sort playlist information
        playlist_response = session.encoded_post(PLAYLIST_URL, {"id": self.id}).json()["playlist"]
        self.title = playlist_response["name"]
        self.creator = playlist_response["creator"]["nickname"]
        self.create_timestamp = playlist_response["createTime"]
        self.last_update_timestamp = playlist_response["updateTime"]
        self.description = playlist_response["description"]
        self.track_count = playlist_response["trackCount"]
        self.tracks = [Music(EncodeSession(), track["id"]) for track in playlist_response["trackIds"]]
        # Deal with tracks in concurrent.futures. Optimized in 0.1.3. Didn't test.
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            per_sum = 10 ** (len(str(self.track_count)) - 1)
            for i in range(0, self.track_count, per_sum):
                futures.append(executor.submit(retail_get,
                                               session,
                                               self.tracks[i:i + per_sum],
                                               quality, detail, file))
            self.tracks = [t for f in futures for t in f.result()]
        if lyric:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in self.tracks:
                    futures.append(executor.submit(i.__init__, session, i.id, quality, lyric))
        """
        if file:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                per_sum = 10 ** (len(str(self.track_count)) - 1)
                for i in range(0, self.track_count, per_sum):
                    futures.append(executor.submit(retail_get_tracks_file, session, self.tracks[i:i + per_sum]))
            self.tracks = [t for f in futures for t in f.result()]
        """