import subprocess
import sys
from Class163_NexT.utils.playwright_login import playwright_login
from Class163_NexT.utils.cookies_manager import save_cookies


def main():
    print("正在执行登录操作...")
    # 执行登录并获取会话
    session = playwright_login()
    
    # 保存会话到cookies文件
    if save_cookies(session):
        print("会话保存成功！")
    else:
        print("会话保存失败！")
        return
    
    print("正在启动FastAPI服务...")
    # 启动FastAPI服务
    try:
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", "16360"],
            check=True
        )
    except KeyboardInterrupt:
        print("服务已停止")
    except Exception as e:
        print(f"启动服务失败: {e}")


if __name__ == "__main__":
    main()
