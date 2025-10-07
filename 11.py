from Class163_NexT.utils import *
from Class163_NexT.models import *

s=load_cookies()
m=Class163(session=s, key_word="https://music.163.com/song?id=2741315465&uct2=U2FsdGVkX1/yoB2EZ72iAN+MTG7iaQbKH92tdDybIEw=")
print(m.music)
