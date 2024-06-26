import requests
import json
import time
import random
import csv

# 信息填写栏
# API URL
comments_api_url = "https://api.bilibili.com/x/v2/reply/wbi/main?oid=1153355619&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=0cbeebd83f02316b10bc2e0661e48099&wts=1719241676"

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
                return response.json()
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

# RUN！
comments_data = fetch_comments(comments_api_url, headers, cookies)

# write
if comments_data and comments_data['code'] == 0:
    comments = comments_data['data']['replies']

    # Open a CSV file to write the data
    with open('comments.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['User', 'Sex', 'Sign', 'Comment', 'Time', 'Location', 'Level'])

        # Parse and write the comments
        for comment in comments:
            user = comment['member']['uname']
            sex = comment['member']['sex']
            sign = comment['member']['sign']
            message = comment['content']['message']
            time_desc = comment['reply_control']['time_desc']
            location = comment['reply_control']['location']
            level = comment['member']['level_info']['current_level']

            # Write the data row
            writer.writerow([user, sex, sign, message, time_desc, location, level])

            # Sleep to avoid being banned
            time.sleep(random.uniform(1, 3))  # Random sleep between 1 and 3 seconds

else:
    print("Failed to retrieve comments")

print(comments_data)