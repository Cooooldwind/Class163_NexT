from fastapi import APIRouter, HTTPException
from Class163_NexT.models import Playlist
from Class163_NexT.utils.cookies_manager import load_cookies
from typing import List, Optional
from datetime import datetime

router = APIRouter()


def format_timestamp(timestamp: int) -> str:
    """将时间戳格式化为可读字符串"""
    if timestamp <= 0:
        return ""
    try:
        dt = datetime.fromtimestamp(timestamp / 1000)  # 网易云时间戳是毫秒
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""

# 获取播放列表信息
@router.get("/info/{playlist_id}", response_model=dict)
async def get_playlist_info(
    playlist_id: int,
    info: bool = True,
    detail: bool = False,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 获取播放列表信息
        playlist = Playlist(session, playlist_id=playlist_id, info=info, detail=detail)
        
        # 获取时间戳并格式化
        create_timestamp = getattr(playlist, "create_timestamp", -1)
        update_timestamp = getattr(playlist, "last_update_timestamp", -1)
        
        # 构建响应数据 - 只使用存在的属性
        response_data = {
            "id": playlist.id,
            "title": playlist.title,
            "creator": playlist.creator,
            "description": playlist.description,
            "track_count": playlist.track_count,
            "create_time": format_timestamp(create_timestamp),
            "update_time": format_timestamp(update_timestamp)
        }
        
        # 如果需要歌曲详情，添加歌曲列表
        if detail:
            songs_data = []
            tracks = getattr(playlist, "tracks", [])
            for song in tracks:
                song_info = {
                    "id": getattr(song, "id", 0),
                    "title": getattr(song, "title", ""),
                    "artists": getattr(song, "artists", []),
                    "album": getattr(song, "album", "")
                }
                songs_data.append(song_info)
            response_data["songs"] = songs_data
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取播放列表信息失败: {str(e)}")

# 获取播放列表歌曲
@router.get("/songs/{playlist_id}", response_model=dict)
async def get_playlist_songs(
    playlist_id: int,
    limit: Optional[int] = None,
    offset: int = 0,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 获取播放列表及其歌曲
        playlist = Playlist(session, playlist_id=playlist_id, info=True, detail=True)
        
        # 获取歌曲列表
        tracks = getattr(playlist, "tracks", [])
        
        # 处理分页
        songs_list = tracks[offset:]
        if limit:
            songs_list = songs_list[:limit]
        
        # 构建响应数据
        songs_data = []
        for song in songs_list:
            song_info = {
                "id": getattr(song, "id", 0),
                "title": getattr(song, "title", ""),
                "artists": getattr(song, "artists", []),
                "album": getattr(song, "album", "")
            }
            songs_data.append(song_info)
        
        response_data = {
            "id": playlist.id,
            "title": playlist.title,
            "total_songs": playlist.track_count,
            "offset": offset,
            "limit": limit,
            "songs": songs_data
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取播放列表歌曲失败: {str(e)}")

# 获取播放列表封面（重定向到封面链接）
@router.get("/cover/{playlist_id}")
async def get_playlist_cover(
    playlist_id: int,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 直接从API获取封面URL
        playlist_response = session.encoded_post("https://music.163.com/weapi/v6/playlist/detail", {"id": playlist_id}).json()["playlist"]
        cover_url = playlist_response.get("coverImgUrl", "")
        
        # 检查是否获取到了有效的URL
        if not cover_url:
            raise HTTPException(status_code=404, detail="未找到播放列表封面链接")
        
        # 直接重定向到封面URL
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=cover_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取播放列表封面失败: {str(e)}")