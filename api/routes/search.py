from fastapi import APIRouter, HTTPException
from Class163_NexT.models import Class163
from Class163_NexT.utils.cookies_manager import load_cookies
from typing import List, Optional

router = APIRouter()

# 搜索音乐和播放列表
@router.get("/", response_model=dict)
async def search(
    keyword: str,
    type: Optional[str] = None,  # 可选值: music, playlist, all
    limit: int = 10,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 创建搜索实例
        search_instance = Class163(session, keyword)
        
        # 构建响应数据
        response_data = {}
        
        # 搜索音乐
        if type in ["music", "all"] or type is None:
            music_results = []
            for music in search_instance.music_search_results[:limit]:
                music_info = {
                    "id": music.id,
                    "title": music.title,
                    "artists": music.artists,
                    "album": music.album
                }
                music_results.append(music_info)
            response_data["music_results"] = music_results
        
        # 搜索播放列表
        if type in ["playlist", "all"] or type is None:
            playlist_results = []
            for playlist in search_instance.playlist_search_results[:limit]:
                playlist_info = {
                    "id": playlist.id,
                    "title": playlist.title,
                    "creator": playlist.creator,
                    "track_count": playlist.track_count
                }
                playlist_results.append(playlist_info)
            response_data["playlist_results"] = playlist_results
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# 搜索音乐
@router.get("/music", response_model=dict)
async def search_music(
    keyword: str,
    limit: int = 10,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 创建搜索实例
        search_instance = Class163(session, keyword)
        
        # 构建音乐搜索结果
        music_results = []
        for music in search_instance.music_search_results[:limit]:
            music_info = {
                "id": music.id,
                "title": music.title,
                "artists": music.artists,
                "album": music.album
            }
            music_results.append(music_info)
        
        return {
            "keyword": keyword,
            "music_results": music_results,
            "total": len(search_instance.music_search_results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索音乐失败: {str(e)}")

# 搜索播放列表
@router.get("/playlist", response_model=dict)
async def search_playlist(
    keyword: str,
    limit: int = 10,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 创建搜索实例
        search_instance = Class163(session, keyword)
        
        # 构建播放列表搜索结果
        playlist_results = []
        for playlist in search_instance.playlist_search_results[:limit]:
            playlist_info = {
                "id": playlist.id,
                "title": playlist.title,
                "creator": playlist.creator,
                "track_count": playlist.track_count
            }
            playlist_results.append(playlist_info)
        
        return {
            "keyword": keyword,
            "playlist_results": playlist_results,
            "total": len(search_instance.playlist_search_results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索播放列表失败: {str(e)}")