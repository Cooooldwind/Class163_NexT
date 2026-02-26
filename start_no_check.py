import subprocess
import sys
from Class163_NexT.utils.cookies_manager import load_cookies


def main():
    print("正在启动 FastAPI 服务...")
    try:
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
        print("服务已停止")
    except Exception as e:
        print(f"启动服务失败: {e}")


if __name__ == "__main__":
    main()
