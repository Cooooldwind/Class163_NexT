from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import re
import requests
import json
import os
import random

router = APIRouter()

# 定义存储邀请链接的文件路径
INVITE_LINKS_FILE = "invite_links.json"

# 确保文件存在
if not os.path.exists(INVITE_LINKS_FILE):
    with open(INVITE_LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

# 验证链接格式和重定向状态
def validate_invite_link(url: str) -> bool:
    # 验证链接格式
    pattern = r'^https://163cn\.tv/[\x00-\x7F]+$'
    if not re.match(pattern, url):
        return False
    
    # 验证重定向状态
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.status_code != 404
    except:
        return False

# 保存邀请链接到文件
def save_invite_link(url: str):
    with open(INVITE_LINKS_FILE, 'r', encoding='utf-8') as f:
        links = json.load(f)
    
    if url not in links:
        links.append(url)
        with open(INVITE_LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=2)

# 获取邀请链接列表
def get_invite_links():
    with open(INVITE_LINKS_FILE, 'r', encoding='utf-8') as f:
        links = json.load(f)
    return links

# 上传邀请链接
@router.get("/upload_invite_link", response_model=dict)
async def upload_invite_link(
    url: str = Query(..., description="邀请链接，格式必须为 https://163cn.tv/XXXXXXX")
):
    try:
        # 验证链接
        is_valid = validate_invite_link(url)
        
        if is_valid:
            # 保存链接
            save_invite_link(url)
            return {"status": "success", "message": "校验通过", "url": url}
        else:
            return {"status": "error", "message": "校验不通过", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

# 获取邀请链接（重定向到随机一个链接）
@router.get("/get_invite_link")
async def get_invite_link():
    try:
        links = get_invite_links()
        if not links:
            raise HTTPException(status_code=404, detail="没有可用的邀请链接")
        
        # 随机选择一个链接
        random_link = random.choice(links)
        
        # 使用307重定向
        return RedirectResponse(url=random_link, status_code=307)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")
