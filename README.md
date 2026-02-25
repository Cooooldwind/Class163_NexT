# Class163\_NexT

[![PyPI version](https://img.shields.io/pypi/v/Class163_NexT?label=Latest)](https://pypi.org/project/class163-next/)
[![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgithub.com%2FCooooldwind%2FClass163_NexT%2Fraw%2Frefs%2Fheads%2Fmain%2Fpyproject.toml
)](https://pypi.org/project/class163-next/)
[![License](https://img.shields.io/pypi/l/class163-next.svg)](https://github.com/Cooooldwind/Class163_NexT/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/CooooldWind/Class163_NexT)](https://github.com/Cooooldwind/Class163_NexT/)



Class163\_NexT 是一个 Python 库，用于操作网易云音乐，包括获取音乐信息、歌词、音乐文件、播放列表以及自动登录管理 Cookies。支持批量处理、多音质下载、内存中处理和本地保存音乐文件。

---

## 功能概览

* **音乐获取**

  * 获取单曲详细信息（标题、歌手、专辑、封面）。
  * 获取歌词（LRC 格式）。
  * 下载音乐文件（支持 MP3、AAC、FLAC 等音质）。
  * 下载专辑封面。
  * 写入音乐文件元数据（ID3 / FLAC）。

* **播放列表管理**

  * 获取播放列表信息（标题、创建者、描述、歌曲列表）。
  * 批量获取歌曲详情、歌词和文件。
  * 并发优化，提高批量处理效率。

* **搜索功能**

  * 根据关键词搜索单曲或播放列表。
  * 支持 ID 或 URL 自动识别。
  * 返回批量搜索结果。

* **登录与 Cookies 管理**

  * 自动检测并加载已保存的 Cookies。
  * Playwright 或 Selenium 自动登录获取网易云音乐 Cookies。
  * 加密存储 Cookies，确保安全。

---

## 安装

通过 PyPI 安装：

```bash
pip install class163-next
```

依赖库：


| 库名                 | 功能               |
|--------------------|------------------|
| mutagen            | 音乐元数据处理          |
 | requests           | 网络请求             |
 | cryptography       | Cookies 加密       |
 | playwright         | 用于 Playwright 登录 |
 | selenium           | 用于 Selenium 登录   |
| netease_encode_api | 创建一个网易云专用登录会话    |

---

## 快速上手

### 1. 登录网易云音乐

```python
from class163_next.utils.playwright_login import playwright_login
session = playwright_login()
```

或者：

```python
from class163_next.utils.selenium_login import selenium_login
session = selenium_login()
```

或加载已保存 Cookies：

```python
from class163_next.utils.cookies_manager import load_cookies
session = load_cookies()
```

---

### 2. 获取单曲信息

```python
from class163_next.models import Music

music = Music(session, music_id=12345678, quality=1, detail=True, lyric=True, file=True)

# 下载文件与封面到内存
music.download_file(session)
music.download_cover(session)

# 保存到本地
music.save("song_name", file=True, cover=True, lyric=True)
```

Class163\_NexT 可以将标题、歌手、专辑、封面等信息写入音乐文件：

```python
# 在下载文件和封面后调用
music.metadata_write()

# 然后再保存
music.save("song_with_metadata", file=True, cover=True, lyric=True)
```

* 对于 MP3 文件，会写入 ID3 标签：标题、歌手、专辑、封面。
* 对于无损 FLAC 文件，会写入 FLAC 元数据和封面。
* 支持歌词导出为 LRC 文件。

---

### 4. 获取播放列表信息

```python
from class163_next.models import Playlist

playlist = Playlist(session, playlist_id=87654321, info=True, detail=True, file=True, lyric=True)
playlist.get_file(session, quality=2)
```

* 并发+批量获取歌曲详情、歌词和文件，提高批量处理速度。

---

### 5. 搜索音乐或播放列表

```python
from class163_next.models import Music163

search = Class163(session, "关键词")
musics = search.music_search_results       # 单曲搜索结果
playlists = search.playlist_search_results # 播放列表搜索结果
```

* 自动识别 ID / URL / 搜索关键词，支持批量搜索和获取详细信息。

---

## 支持音质

| 序号 | 显示名    | API命名    | 编码格式       | 码率              |
|----|--------|----------|------------|-----------------|
| 1  | 标准     | standard | mp3        | 128kbps         |
| 2  | 较高     | higher   | mp3        | 192kbps         |
| 3  | 极高     | exhigh   | mp3        | 320kbps         |
| 4  | 无损     | lossless | aac (flac) | 最高 48kHz/16bit  |
| 5  | 高解析度无损 | hires    | aac (flac) | 最高 192kHz/24bit |
| 6  | 高清臻音   | jyeffect | aac (flac) | 96kHz/24bit     |
| 7  | 超清母带   | jymaster | aac (flac) | 192kHz/24bit    |

###### 备注：较高音质已经从客户端消失了；高清臻音和超清母带格式可能会有 AI 合成的参与（强行拉到相应码率），而无损和高解析度无损只会对版权方上传的码率过高的音频做压缩处理。

---

## 安全与注意事项

* Cookies 会加密存储在 `~/.class163_next_cookies`。
* 确保系统已安装对应浏览器（Chromium / Edge）用于自动登录。（对于该点，仍需大量测试验证）
* 批量下载大文件时，请注意内存使用，可通过 `clean=True` 清理内存数据。

---

## 免责声明

Class163\_NexT 仅提供技术工具**用于学习、研究和个人备份用途**。用户必须自行确保对本 Python 库及其产生的任何文件的使用符合当地法律法规以及网易云音乐的服务条款。
**开发者不对任何违反版权或非法分发音乐文件的行为承担责任。**
请勿将**本 Python 库及其生成的任何文件**用于商业用途或未经授权的公开分发。
请妥善保管我们替您存储在 `~/.class163_next_cookies` 里面的**所有文件**。因不妥善保管导致用户信息泄露造成的后果**应由用户自行承担**。

---

###### Written by $CooooldWind$ & $ChatGPT^{TM}$.