FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY Class163_NexT/ ./Class163_NexT/
COPY Class163_NexT_API/ ./Class163_NexT_API/

EXPOSE 16360

CMD ["python", "-m", "uvicorn", "Class163_NexT_API.main:app", "--host", "0.0.0.0", "--port", "16360"]
