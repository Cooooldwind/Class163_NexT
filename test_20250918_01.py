import time
from pprint import pprint

# from Class163_NexT.models.playlist import Playlist
from Class163_NexT.utils import *


s = load_cookies()

encode_data = {"s": "五月天","type": 1000,"offset": "100","total": "true","limit": "100"}
detail_response = s.encoded_post("https://music.163.com/weapi/cloudsearch/get/web",encode_data)
pprint(detail_response.json()["result"])