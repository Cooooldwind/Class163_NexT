from Class163_NexT.utils import *
from Class163_NexT.models import *

s=load_cookies()
m=Class163(session=s, key_word="https://music.163.com/song?id=2736357221&uct2=U2FsdGVkX1+weggm/0rvf39i6D1acETMcNHwdT0tLfY=")
m=m.music
m.get_detail(session=s)
m.quality = 6
m.download_cover(s, pixel=600)
m.save("test", cover=True)
print(m.quality)
