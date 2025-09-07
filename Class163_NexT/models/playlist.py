import concurrent.futures
from netease_encode_api import EncodeSession
from .music import Music

PLAYLIST_URL = "https://music.163.com/weapi/v6/playlist/detail"

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
        # Deal with tracks in concurrent.futures
        threadpool = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in self.tracks:
                threadpool.append(executor.submit(i.__init__, session, i.id, quality, detail, lyric, file))
