import time

from Class163_NexT.models.playlist import Playlist
from Class163_NexT.selenium_login import selenium_login

start_time = time.time()
s = selenium_login()
end_time = time.time()
print("Login:",end="")
print(end_time - start_time)

start_time = time.time()
pl2 = Playlist(s, 2391850012, detail=True, new=True)
sum2 = 0
for t in pl2.tracks:
    sum2 += 1
    print(str(sum2) + ": " + t.title)
end_time = time.time()
print("New:",end="")
print(end_time - start_time)