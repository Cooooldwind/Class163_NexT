# Docker 部署指南

## 快速开始

### 使用 Docker Compose（推荐）

1. 确保本地已保存 cookies（通过 `start.py` 或 `playwright_login` 登录后保存）
2. 启动服务：
```bash
docker-compose up -d
```

3. 查看日志：
```bash
docker-compose logs -f
```

4. 停止服务：
```bash
docker-compose down
```

### 使用 Docker 命令

1. 构建镜像：
```bash
docker build -t class163-next-api .
```

2. 运行容器：
```bash
docker run -d \
  --name class163-next-api \
  -p 16360:16360 \
  -v ~/.class163_next_key:/root/.class163_next_key \
  -v ~/.class163_next_cookies:/root/.class163_next_cookies \
  class163-next-api
```

3. 查看日志：
```bash
docker logs -f class163-next-api
```

4. 停止容器：
```bash
docker stop class163-next-api
```

## Cookies 管理

容器通过挂载本地 cookies 文件来保持登录状态：
- `~/.class163_next_key` - 加密密钥文件
- `~/.class163_next_cookies` - 加密的 cookies 文件

如果 cookies 过期，请在本地重新登录并保存 cookies，然后重启容器。

## API 访问

服务启动后，可以通过以下地址访问：
- API 文档：http://localhost:16360/docs
- ReDoc 文档：http://localhost:16360/redoc
- 根路径：http://localhost:16360/

## 环境变量

当前版本无需额外环境变量配置，所有配置均使用默认值。

## 注意事项

- 容器不会自动登录，需要提前在本地保存 cookies
- 确保 cookies 文件有正确的权限
- 如需更新代码，重新构建镜像即可
