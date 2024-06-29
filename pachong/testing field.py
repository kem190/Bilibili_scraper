import time
import hashlib
from urllib.parse import quote
import re

timestamp = (time.time() * 1000)
pagination_str =  f"{"offset":"{\\"type\\":1,\\"direction\":1,\\"session_id\\":\\"{id_from_previous_page}\\",\\"data\\":{}}"}"



url = (f"https://api.bilibili.com/x/v2/reply/wbi/main?oid=47527629&type=1&mode=3&pagination_str={pagination_str}&plat=1&web_location=1315875&w_rid={w_rid}&wts={timestamp}")