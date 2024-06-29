import requests
import json
import time
import random
import csv
import hashlib
from urllib.parse import quote
import re

# 信息填写栏
# API URL
comments_api_url = "https://api.bilibili.com/x/v2/reply/wbi/main?oid=1505922100&type=1&mode=3&pagination_str=%7B%22offset%22:%22%7B%5C%22type%5C%22:1,%5C%22direction%5C%22:1,%5C%22session_id%5C%22:%5C%221760931494753896%5C%22,%5C%22data%5C%22:%7B%7D%7D%22%7D&plat=1&web_location=1315875&w_rid=920d09a5d1bb90a38e6881a37bf79e2f&wts=1719659679"

# Cookies (这是我自己的账号需要替换)
cookies = {
    "Cookies": "buvid3=E579EDE8-64A3-72D3-AD0D-9A111BE54DD103395infoc; b_nut=1713522703; CURRENT_FNVAL=4048; _uuid=A410CC8A5-FF13-FF86-D6FA-3542F4CC4910F05666infoc; buvid4=346F68FE-9DBC-DD3B-F9B3-C82EF884743305819-024041910-AYCtu957i4E2ZljBHTFxVg%3D%3D; rpdid=|(uJ~l)lmJ~R0J'u~uJlkk~ul; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NEW_POP; header_theme_version=CLOSE; buvid_fp_plain=undefined; DedeUserID=37424969; DedeUserID__ckMd5=02c3aef233c2afc9; PVID=1; fingerprint=7bc8ecec0e75401f907a3d6629ab4e69; buvid_fp=7bc8ecec0e75401f907a3d6629ab4e69; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTkyNjg2MTMsImlhdCI6MTcxOTAwOTM1MywicGx0IjotMX0.-LdByVQmu-_jQFzpGDFqMQcqNBAarAowkZWJgTFfta0; bili_ticket_expires=1719268553; SESSDATA=a78c20de%2C1734696255%2Cb4d7d%2A62CjAlG5VbsUom3wUMggQRRW4gH-Dla6slK6SjWQ0o0NWZYcL4vZeHnmode7f2aL38tDYSVnVBRXoyWVM3S0xQWFVJbUc5TzMxMWlBaFdNRkEtY0JSSHgzeFhJTlhPaDhwX0htdHJjU3NDMnRnTGVIc1d0eWxwUE5rVWtTZEpnMHJUZ1dRanI5NnhBIIEC; bili_jct=c4704f6d7e6253cd5671c1d19e2d9cc0; sid=84sbggfc; home_feed_column=5; browser_resolution=1707-940; CURRENT_QUALITY=80; bp_t_offset_37424969=946595446120251392; b_lsid=B6BAF423_1904AA658CD; bsource=search_google"
}

# 准备工作
# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive"
}


def fetch_comments(api_url, headers, cookies, retries=3):
    for i in range(retries):
        try:
            response = requests.get(api_url, headers=headers, cookies=cookies)
            if response.status_code == 200:
                data = response.json()
                with open('vector.json', 'w') as file:
                    json.dump(data, file)
                    return data
            elif response.status_code == 429:  # Too Many Requests
                wait_time = int(response.headers.get("Retry-After", 2 ** i))
                print(f"Rate limited. Waiting for {wait_time} seconds.")
                time.sleep(wait_time)
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        time.sleep(2 ** i + random.random())  # Exponential backoff with jitter
    return None


def extract_comment_data(comment):
    user = comment['member']['uname']
    sex = comment['member']['sex']
    sign = comment['member']['sign']
    message = comment['content']['message']
    time_desc = comment['reply_control']['time_desc']
    location = comment['reply_control'].get('location', '')
    level = comment['member']['level_info']['current_level']
    return {
        "user": user,
        "sex": sex,
        "sign": sign,
        "message": message,
        "time_desc": time_desc,
        "location": location,
        "level": level
    }
def gen_url_key(pagination_str, timestamp):
    ee = [
        "mode=3",
        "oid=758385725",
        f"pagination_str={quote(pagination_str)}",
        "plat=1",
        "type=1",
        "web_location=1315875",
        f"wts={timestamp}"
    ]
    z = 'ea1db124af3c7062474693fa704f4ff8'
    L = '&'.join(ee)
    MD5 = hashlib.md5()
    last_key = L + z
    MD5.update(last_key.encode('utf-8'))
    w_rid = MD5.hexdigest()
    return w_rid


# RUN！
all_data = fetch_comments(comments_api_url, headers, cookies)

# write
if all_data and all_data['code'] == 0:
    comments = all_data['data']['replies']

    # 会返回错误的gen_url
    # next_offset = all_data['data']['cursor']['pagination_reply']['next_offset']
    # print(next_offset)
    # id_next_page = re.findall('session_id\":(\d+)', all_data)[0]
    # print(id_next_page)
    # pagination_str = f'{{"offset": {{"type": 1, "direction": 1, "session_id": "{id_next_page}", "data": {{}}}}}}'
    # # pagination_str = f"{"offset":"{\\"type\\": 1, \\"direction\":1,\\"session_id\\":\\"{id_next_page}\\",\\"data\\":{}}"}"
    # timestamp = time.time()
    # w_rid = gen_url_key(pagination_str, timestamp)
    # new_url = (
    #     f"https://api.bilibili.com/x/v2/reply/wbi/main?oid=47527629&type=1&mode=3&pagination_str={pagination_str}&plat=1&web_location=1315875&w_rid={w_rid}&wts={timestamp}")
    # print(new_url)
    comments_list = []

    # Parse and structure the comments data
    for comment in comments:
        parent_data = extract_comment_data(comment)
        parent_data['replies'] = []

        if 'replies' in comment:
            for reply in comment['replies'][:3]:  # Get top 3 replies
                child_data = extract_comment_data(reply)
                parent_data['replies'].append(child_data)

        comments_list.append(parent_data)

        # Sleep to avoid being banned
        time.sleep(random.uniform(1, 3))  # Random sleep between 1 and 3 seconds

    # Write to a JSON file
    with open('comments.json', 'w', encoding='utf-8') as json_file:
        json.dump(comments_list, json_file, ensure_ascii=False, indent=4)

else:
    print("Failed to retrieve comments")
