from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import music, playlist, search
from Class163_NexT.utils.cookies_manager import load_cookies
from Class163_NexT.models import Music, Playlist, Class163

app = FastAPI(
    title="Class163_NexT API",
    description="网易云音乐操作接口集，支持获取音乐信息、歌词、播放列表等功能",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(music.router, prefix="/api/music", tags=["音乐"])
app.include_router(playlist.router, prefix="/api/playlist", tags=["播放列表"])
app.include_router(search.router, prefix="/api/search", tags=["搜索"])

@app.get("/")
async def root():
    return {"message": "Class163_NexT API 服务运行中"}

@app.get("/health")
async def health_check():
    session = load_cookies()
    has_session = session is not None
    
    endpoints = {
        "music_info": {"name": "音乐信息", "path": "/api/music/info/{music_id}", "available": False, "message": ""},
        "music_file": {"name": "音乐文件", "path": "/api/music/file/{music_id}", "available": False, "message": ""},
        "music_lyric": {"name": "音乐歌词", "path": "/api/music/lyric/{music_id}", "available": False, "message": ""},
        "music_cover": {"name": "音乐封面", "path": "/api/music/cover/{music_id}", "available": False, "message": ""},
        "playlist_info": {"name": "歌单信息", "path": "/api/playlist/info/{playlist_id}", "available": False, "message": ""},
        "playlist_songs": {"name": "歌单歌曲", "path": "/api/playlist/songs/{playlist_id}", "available": False, "message": ""},
        "playlist_cover": {"name": "歌单封面", "path": "/api/playlist/cover/{playlist_id}", "available": False, "message": ""},
        "search": {"name": "搜索", "path": "/api/search/", "available": False, "message": ""},
        "search_music": {"name": "搜索音乐", "path": "/api/search/music", "available": False, "message": ""},
        "search_playlist": {"name": "搜索歌单", "path": "/api/search/playlist", "available": False, "message": ""}
    }
    
    if not has_session:
        for key in endpoints:
            endpoints[key]["message"] = "未找到有效会话，请先登录"
    else:
        try:
            Music(session, music_id=1, detail=True)
            endpoints["music_info"]["available"] = True
            endpoints["music_info"]["message"] = "正常"
        except Exception as e:
            endpoints["music_info"]["message"] = f"异常: {str(e)}"
        
        try:
            music = Music(session, music_id=1, detail=True, file=True)
            music.get_file(session)
            endpoints["music_file"]["available"] = True
            endpoints["music_file"]["message"] = "正常"
        except Exception as e:
            endpoints["music_file"]["message"] = f"异常: {str(e)}"
        
        try:
            Music(session, music_id=1, lyric=True)
            endpoints["music_lyric"]["available"] = True
            endpoints["music_lyric"]["message"] = "正常"
        except Exception as e:
            endpoints["music_lyric"]["message"] = f"异常: {str(e)}"
        
        try:
            Music(session, music_id=1, detail=True)
            endpoints["music_cover"]["available"] = True
            endpoints["music_cover"]["message"] = "正常"
        except Exception as e:
            endpoints["music_cover"]["message"] = f"异常: {str(e)}"
        
        try:
            Playlist(session, playlist_id=1, info=True, detail=False)
            endpoints["playlist_info"]["available"] = True
            endpoints["playlist_info"]["message"] = "正常"
        except Exception as e:
            endpoints["playlist_info"]["message"] = f"异常: {str(e)}"
        
        try:
            Playlist(session, playlist_id=1, info=True, detail=True)
            endpoints["playlist_songs"]["available"] = True
            endpoints["playlist_songs"]["message"] = "正常"
        except Exception as e:
            endpoints["playlist_songs"]["message"] = f"异常: {str(e)}"
        
        try:
            session.encoded_post("https://music.163.com/weapi/v6/playlist/detail", {"id": 1}).json()
            endpoints["playlist_cover"]["available"] = True
            endpoints["playlist_cover"]["message"] = "正常"
        except Exception as e:
            endpoints["playlist_cover"]["message"] = f"异常: {str(e)}"
        
        try:
            Class163(session, "test")
            endpoints["search"]["available"] = True
            endpoints["search"]["message"] = "正常"
        except Exception as e:
            endpoints["search"]["message"] = f"异常: {str(e)}"
        
        try:
            Class163(session, "test")
            endpoints["search_music"]["available"] = True
            endpoints["search_music"]["message"] = "正常"
        except Exception as e:
            endpoints["search_music"]["message"] = f"异常: {str(e)}"
        
        try:
            Class163(session, "test")
            endpoints["search_playlist"]["available"] = True
            endpoints["search_playlist"]["message"] = "正常"
        except Exception as e:
            endpoints["search_playlist"]["message"] = f"异常: {str(e)}"
    
    available_count = sum(1 for ep in endpoints.values() if ep["available"])
    total_count = len(endpoints)
    
    return {
        "status": "healthy",
        "session": {
            "available": has_session,
            "message": "会话有效" if has_session else "未找到有效会话，请先登录"
        },
        "endpoints": endpoints,
        "summary": {
            "total": total_count,
            "available": available_count,
            "unavailable": total_count - available_count
        }
    }