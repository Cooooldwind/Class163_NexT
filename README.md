# Class163_NexT

之前的 [史山class163](https://github.com/cooooldwind/class163) 我已经不太想维护了，所以就开了这个新仓库。

这个库是基于 Python 3.13.7写的。所以我只推荐 Python 3.13.* 用这个库。这阵子我会想办法测试这个库的最低兼容版本的。

## 安装

`pip install Class163_NexT`

或者安装 Python 3.13+ 然后直接下载整个仓库的 ZIP 文件到本地解压。

啊对就是这么简单（（（

## 使用

这是一个很普通的脚本，你可以在 `test_20250907_01.py` 找到。

```python
from Class163_NexT.models.music import Music
from Class163_NexT.selenium_login import selenium_login

session = selenium_login()
music = Music(session=session, music_id=2621539078, quality=4, detail=True, lyric=True, file=True)
print(music.music_url)
music.download_music()
```

接下来我将解释每行的用途：

前两行引入 `Music` 类和 `selenium_login` 函数。

`selenium_login` 目前只支持 Chromium 内核的 Edge 浏览器。

第三行空行。

第四行运行的时候会下载 `msedgedriver.exe` 然后用它串联起 Edge 前端和咱这后端，调起一个网易云登录页面。

登录后，用户信息存在 `session` 变量， `msedgedriver.exe` 自动删除。

**您的用户凭证不会被上传到任何地方，程序结束后将自动清除。也请不要获得 `session` 里面的与用户凭证相关的资料并传输给他人或直接发在网上。**

第5行是获取 id 为 `2621539078` 的歌曲信息。

`detail`，`lyric` 和 `file` 分别代表歌曲信息、歌词、歌曲文件。将这些值传入 `True` 才会执行命令。

`quality` 是歌曲音质，只有 1~4 四个数字可选。

从小到大分别对应：

- 标准

- 较高（网易云客户端没有这个选项）

- 极高

- 无损

`session` 是必须传入的，传入的值就是刚刚 `selenium_login` 返回的值。

接下来打印歌曲文件的链接。

最后一行是下载歌曲。可以传入 `filename` 指定文件名称。

**好的，看懂以上内容就说明你已经会用了，快去下载自己的歌曲吧。**
