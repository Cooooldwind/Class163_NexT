FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && \
    playwright install && \
    playwright install-deps
EXPOSE 16360

CMD ["python", "start.py"]