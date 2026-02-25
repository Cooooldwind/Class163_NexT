"""
API测试文件
不使用任何外部库，仅使用Python标准库
"""
import urllib.request
import urllib.parse
import json
import sys

# 基础配置
BASE_URL = "http://127.0.0.1:16360"
TEST_MUSIC_ID = 3342707944
TEST_PLAYLIST_ID = 2391850012
TEST_KEYWORD = "トゲナシトゲアリ"


def make_request(url, method="GET", data=None):
    """发送HTTP请求并返回响应"""
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header('Content-Type', 'application/json')
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            headers = dict(response.headers)
            
            # 检查是否是重定向响应 (302, 307, 308)
            if status_code in [301, 302, 303, 307, 308]:
                return {
                    "status_code": status_code,
                    "is_redirect": True,
                    "redirect_url": headers.get('Location', ''),
                    "headers": headers
                }
            
            content_type = headers.get('Content-Type', '')
            raw_body = response.read()
            
            # 如果是图片或二进制数据
            if 'image' in content_type or 'audio' in content_type:
                return {
                    "status_code": status_code,
                    "is_binary": True,
                    "content_type": content_type,
                    "content_length": len(raw_body),
                    "headers": headers
                }
            
            # 尝试解码为文本
            try:
                body = raw_body.decode('utf-8')
            except UnicodeDecodeError:
                # 如果不是UTF-8，可能是二进制数据
                return {
                    "status_code": status_code,
                    "is_binary": True,
                    "content_type": content_type,
                    "content_length": len(raw_body),
                    "headers": headers
                }
            
            try:
                json_body = json.loads(body)
            except:
                json_body = body
            
            return {
                "status_code": status_code,
                "is_redirect": False,
                "body": json_body,
                "headers": headers
            }
    except urllib.error.HTTPError as e:
        error_body = e.read()
        try:
            decoded_body = error_body.decode('utf-8')
        except:
            decoded_body = str(error_body)
        return {
            "status_code": e.code,
            "error": True,
            "body": decoded_body
        }
    except Exception as e:
        return {
            "status_code": -1,
            "error": True,
            "body": str(e)
        }


def print_result(test_name, result):
    """打印测试结果"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")
    
    if result.get("error"):
        print(f"状态码: {result['status_code']}")
        print(f"错误: {result['body']}")
    elif result.get("is_redirect"):
        print(f"状态码: {result['status_code']}")
        print(f"重定向URL: {result['redirect_url']}")
        print("✓ 重定向成功")
    elif result.get("is_binary"):
        print(f"状态码: {result['status_code']}")
        print(f"内容类型: {result['content_type']}")
        print(f"内容大小: {result['content_length']} bytes")
        print("✓ 二进制数据接收成功")
    else:
        print(f"状态码: {result['status_code']}")
        if isinstance(result['body'], dict):
            print(f"响应体:\n{json.dumps(result['body'], ensure_ascii=False, indent=2)}")
        else:
            print(f"响应体: {result['body']}")
        
        # 检查是否有错误
        if isinstance(result['body'], dict) and 'detail' in result['body']:
            print("✗ 测试失败")
        else:
            print("✓ 测试通过")


def test_health():
    """测试健康检查接口"""
    url = f"{BASE_URL}/health"
    result = make_request(url)
    print_result("健康检查", result)
    return result.get("status_code") == 200


def test_music_info():
    """测试获取音乐信息"""
    url = f"{BASE_URL}/api/music/info/{TEST_MUSIC_ID}"
    result = make_request(url)
    print_result(f"获取音乐信息 (ID: {TEST_MUSIC_ID})", result)
    return result.get("status_code") == 200


def test_music_file():
    """测试获取音乐文件（重定向）"""
    url = f"{BASE_URL}/api/music/file/{TEST_MUSIC_ID}?quality=1"
    result = make_request(url)
    print_result(f"获取音乐文件 (ID: {TEST_MUSIC_ID})", result)
    return result.get("status_code") in [200, 301, 302, 303, 307, 308] or result.get("is_redirect") or result.get("is_binary")


def test_music_lyric():
    """测试获取音乐歌词"""
    url = f"{BASE_URL}/api/music/lyric/{TEST_MUSIC_ID}"
    result = make_request(url)
    print_result(f"获取音乐歌词 (ID: {TEST_MUSIC_ID})", result)
    return result.get("status_code") == 200


def test_music_cover():
    """测试获取音乐封面（重定向）"""
    url = f"{BASE_URL}/api/music/cover/{TEST_MUSIC_ID}"
    result = make_request(url)
    print_result(f"获取音乐封面 (ID: {TEST_MUSIC_ID})", result)
    return result.get("status_code") in [200, 301, 302, 303, 307, 308] or result.get("is_redirect") or result.get("is_binary")


def test_playlist_info():
    """测试获取播放列表信息"""
    url = f"{BASE_URL}/api/playlist/info/{TEST_PLAYLIST_ID}"
    result = make_request(url)
    print_result(f"获取播放列表信息 (ID: {TEST_PLAYLIST_ID})", result)
    return result.get("status_code") == 200


def test_playlist_info_with_detail():
    """测试获取播放列表信息（包含歌曲详情）"""
    url = f"{BASE_URL}/api/playlist/info/{TEST_PLAYLIST_ID}?detail=true"
    result = make_request(url)
    print_result(f"获取播放列表信息(含详情) (ID: {TEST_PLAYLIST_ID})", result)
    return result.get("status_code") == 200


def test_playlist_songs():
    """测试获取播放列表歌曲"""
    url = f"{BASE_URL}/api/playlist/songs/{TEST_PLAYLIST_ID}?limit=5&offset=0"
    result = make_request(url)
    print_result(f"获取播放列表歌曲 (ID: {TEST_PLAYLIST_ID})", result)
    return result.get("status_code") == 200


def test_playlist_cover():
    """测试获取播放列表封面"""
    url = f"{BASE_URL}/api/playlist/cover/{TEST_PLAYLIST_ID}"
    result = make_request(url)
    print_result(f"获取播放列表封面 (ID: {TEST_PLAYLIST_ID})", result)
    return result.get("status_code") == 200


def test_search():
    """测试搜索"""
    encoded_keyword = urllib.parse.quote(TEST_KEYWORD)
    url = f"{BASE_URL}/api/search/?keyword={encoded_keyword}&limit=5"
    result = make_request(url)
    print_result(f"搜索 (关键词: {TEST_KEYWORD})", result)
    return result.get("status_code") == 200


def test_search_music():
    """测试搜索音乐"""
    encoded_keyword = urllib.parse.quote(TEST_KEYWORD)
    url = f"{BASE_URL}/api/search/music?keyword={encoded_keyword}&limit=5"
    result = make_request(url)
    print_result(f"搜索音乐 (关键词: {TEST_KEYWORD})", result)
    return result.get("status_code") == 200


def test_search_playlist():
    """测试搜索播放列表"""
    encoded_keyword = urllib.parse.quote(TEST_KEYWORD)
    url = f"{BASE_URL}/api/search/playlist?keyword={encoded_keyword}&limit=5"
    result = make_request(url)
    print_result(f"搜索播放列表 (关键词: {TEST_KEYWORD})", result)
    return result.get("status_code") == 200


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("API 测试开始")
    print("="*60)
    print(f"基础URL: {BASE_URL}")
    print(f"测试歌曲ID: {TEST_MUSIC_ID}")
    print(f"测试歌单ID: {TEST_PLAYLIST_ID}")
    print(f"测试搜索关键词: {TEST_KEYWORD}")
    
    results = []
    
    # 基础测试
    print("\n" + "-"*60)
    print("基础接口测试")
    print("-"*60)
    results.append(("健康检查", test_health()))
    
    # 音乐接口测试
    print("\n" + "-"*60)
    print("音乐接口测试")
    print("-"*60)
    results.append(("音乐信息", test_music_info()))
    results.append(("音乐文件", test_music_file()))
    results.append(("音乐歌词", test_music_lyric()))
    results.append(("音乐封面", test_music_cover()))
    
    # 播放列表接口测试
    print("\n" + "-"*60)
    print("播放列表接口测试")
    print("-"*60)
    results.append(("歌单信息", test_playlist_info()))
    results.append(("歌单信息(含详情)", test_playlist_info_with_detail()))
    results.append(("歌单歌曲", test_playlist_songs()))
    results.append(("歌单封面", test_playlist_cover()))
    
    # 搜索接口测试
    print("\n" + "-"*60)
    print("搜索接口测试")
    print("-"*60)
    results.append(("搜索", test_search()))
    results.append(("搜索音乐", test_search_music()))
    results.append(("搜索歌单", test_search_playlist()))
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    failed = sum(1 for _, r in results if not r)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {name}")
    
    print(f"\n总计: {len(results)} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    
    if failed == 0:
        print("\n🎉 所有测试通过!")
    else:
        print(f"\n⚠️ 有 {failed} 个测试失败")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
