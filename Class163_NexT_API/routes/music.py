from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from Class163_NexT.models import Music
from Class163_NexT.utils.cookies_manager import load_cookies
from typing import Optional

router = APIRouter()

# 获取音乐信息
@router.get("/info/{music_id}", response_model=dict)
async def get_music_info(
    music_id: int,
    detail: bool = True,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 获取音乐信息（detail模式下不获取lyric）
        music = Music(session, music_id=music_id, detail=detail)
        
        # 构建响应数据
        response_data = {
            "id": music.id,
            "title": music.title,
            "artists": music.artists,
            "album": music.album,
            "cover_url": music.cover_url
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取音乐信息失败: {str(e)}")

# 获取音乐文件（重定向到下载链接）
@router.get("/file/{music_id}")
async def get_music_file(
    music_id: int,
    quality: int = 1,  # 1: 标准, 2: 较高, 3: 极高, 4: 无损, 5: 高解析度无损
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 获取音乐信息和文件URL
        music = Music(session, music_id=music_id, detail=True, file=True)
        music.quality = quality  # 设置音质
        music.get_file(session)  # 获取音乐文件URL
        
        # 检查是否获取到了有效的URL
        if not music.music_url:
            raise HTTPException(status_code=404, detail="未找到音乐文件链接")
        
        # 直接重定向到音乐文件URL
        return RedirectResponse(url=music.music_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取音乐文件失败: {str(e)}")

# 获取音乐歌词
@router.get("/lyric/{music_id}", response_model=dict)
async def get_music_lyric(
    music_id: int,
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 获取音乐歌词
        music = Music(session, music_id=music_id, lyric=True)
        
        # 构建响应数据
        response_data = {
            "id": music.id,
            "title": music.title,
            "artists": music.artists,
            "lyric": music.lyric
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取音乐歌词失败: {str(e)}")

# 获取音乐封面（重定向到封面链接）
@router.get("/cover/{music_id}")
async def get_music_cover(
    music_id: int,
    pixel: int = -1,  # 图片边长，若不填，图片边长将由网站决定
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 获取音乐信息和封面URL
        music = Music(session, music_id=music_id, detail=True)
        
        # 检查是否获取到了有效的URL
        if not music.cover_url:
            raise HTTPException(status_code=404, detail="未找到音乐封面链接")
        
        # 构建完整的封面URL（包含像素参数）
        cover_url = f"{music.cover_url}?param={pixel}y{pixel}" if pixel > 0 else music.cover_url
        
        # 直接重定向到封面URL
        return RedirectResponse(url=cover_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取音乐封面失败: {str(e)}")