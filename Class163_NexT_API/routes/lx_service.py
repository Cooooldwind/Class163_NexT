from fastapi import APIRouter, HTTPException
from Class163_NexT.models import Music
from Class163_NexT.utils.cookies_manager import load_cookies

router = APIRouter()

# 获取歌曲链接
@router.get("/get", response_model=dict)
async def get_lx_service(
    id: int,
    qualify: int = 1,  # 1: 标准, 2: 较高, 3: 极高, 4: 无损, 5: 高解析度无损
):
    try:
        # 加载会话
        session = load_cookies()
        if not session:
            raise HTTPException(status_code=401, detail="未找到有效会话，请先登录")
        
        # 获取音乐信息和文件URL
        music = Music(session, music_id=id, detail=True, file=True)
        music.quality = qualify  # 设置音质
        music.get_file(session)  # 获取音乐文件URL
        
        # 检查是否获取到了有效的URL
        if not music.music_url:
            raise HTTPException(status_code=404, detail="未找到音乐文件链接")
        
        # 构建响应数据，只包含url字段
        response_data = {
            "url": music.music_url
        }
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取音乐文件失败: {str(e)}")
