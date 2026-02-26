from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import music, playlist, search, lx_service
from Class163_NexT.utils.cookies_manager import load_cookies
from Class163_NexT.models import Music, Playlist, Class163
import uvicorn
import logging

# 配置uvicorn日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 获取uvicorn日志记录器
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers[0].setFormatter(
    logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
                     datefmt='%Y-%m-%d %H:%M:%S')
)

app = FastAPI(
    title="Class163_NexT API",
    description="网易云音乐操作接口集，支持获取音乐信息、歌词、播放列表等功能",
    version="0.2.2",
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
app.include_router(lx_service.router, prefix="/api/lx_service", tags=["洛雪API服务"])

@app.get("/")
async def root():
    return {"message": "Class163_NexT API 服务运行中"}
