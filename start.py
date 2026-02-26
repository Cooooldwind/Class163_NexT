import subprocess
import sys
import logging
from Class163_NexT.utils.playwright_login import playwright_login
from Class163_NexT.utils.cookies_manager import save_cookies, load_cookies
from Class163_NexT.models import Class163, Music

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def test_search():
    """使用Class163_NexT库测试搜索功能"""
    logger.info("正在测试搜索功能...")
    session = load_cookies()
    if not session:
        logger.error("无法加载会话，搜索测试失败")
        return None
    
    try:
        # 使用Class163库进行搜索
        search_instance = Class163(session, "ノンブレス・オブリージュ")
        if search_instance.music_search_results and len(search_instance.music_search_results) > 0:
            logger.info("搜索功能测试成功！")
            return search_instance.music_search_results[0]
        else:
            logger.warning("搜索功能返回空结果")
            return None
    except Exception as e:
        logger.error(f"测试搜索功能时出错: {e}")
        return None


def test_download(song_id):
    """使用Class163_NexT库测试下载功能"""
    logger.info(f"正在测试下载功能 (歌曲ID: {song_id})...")
    session = load_cookies()
    if not session:
        logger.error("无法加载会话，下载测试失败")
        return False
    
    try:
        # 使用Music库获取音乐文件URL
        music = Music(session, music_id=song_id, detail=True, file=True)
        music.quality = 4  # 设置音质为高音质
        music.get_file(session)
        
        if music.music_url:
            logger.info("下载功能测试成功！")
            return True
        else:
            logger.error("下载功能测试失败，未获取到音乐URL")
            return False
    except Exception as e:
        logger.error(f"测试下载功能时出错: {e}")
        return False


def main():
    # 1. 尝试加载cookies
    logger.info("正在尝试加载cookies...")
    session = load_cookies()
    
    # 2. 如果cookies加载失败，执行登录
    if not session:
        logger.info("cookies加载失败，执行登录操作...")
        session = playwright_login()
        
        # 保存会话到cookies文件
        if save_cookies(session):
            logger.info("会话保存成功！")
        else:
            logger.error("会话保存失败！")
            return
    else:
        logger.info("cookies加载成功！")
    
    # 3. 测试搜索功能
    song = test_search()
    if not song:
        logger.warning("搜索功能测试失败，重新执行登录...")
        session = playwright_login()
        if save_cookies(session):
            logger.info("会话重新保存成功！")
            # 再次测试搜索功能
            song = test_search()
            if not song:
                logger.error("搜索功能仍然失败，无法继续测试")
        else:
            logger.error("会话重新保存失败！")
    
    # 4. 测试下载功能
    if song:
        success = test_download(song.id)
        if not success:
            logger.warning("警告：可能没有VIP权限")
    
    # 5. 启动FastAPI服务
    logger.info("正在启动FastAPI服务...")
    try:
        # 启动服务
        subprocess.run(
            [
                sys.executable, 
                "-m", 
                "uvicorn", 
                "Class163_NexT_API.main:app", 
                "--reload", 
                "--port", 
                "16360"
            ],
            check=True
        )
    except KeyboardInterrupt:
        logger.info("服务已停止")
    except Exception as e:
        logger.error(f"启动服务失败: {e}")


if __name__ == "__main__":
    main()
