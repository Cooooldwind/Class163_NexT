import traceback
from functools import wraps

def safe_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            # 打印完整堆栈信息，不抛出异常
            traceback.print_exc()
            return None
    return wrapper
