import requests
import json
from time import sleep

def fetch_comments(api_url, headers, cookies, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(api_url, headers=headers, cookies=cookies)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch data: {response.status_code}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
        sleep(1)  # Wait for 1 second before retrying
    return None

# Example headers and cookies, replace with actual values
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.bilibili.com/',
    'X-Requested-With': 'XMLHttpRequest'
}

cookies = {
    "Cookies": "buvid3=E579EDE8-64A3-72D3-AD0D-9A111BE54DD103395infoc; b_nut=1713522703; CURRENT_FNVAL=4048; _uuid=A410CC8A5-FF13-FF86-D6FA-3542F4CC4910F05666infoc; buvid4=346F68FE-9DBC-DD3B-F9B3-C82EF884743305819-024041910-AYCtu957i4E2ZljBHTFxVg%3D%3D; rpdid=|(uJ~l)lmJ~R0J'u~uJlkk~ul; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NEW_POP; header_theme_version=CLOSE; buvid_fp_plain=undefined; DedeUserID=37424969; DedeUserID__ckMd5=02c3aef233c2afc9; PVID=1; fingerprint=7bc8ecec0e75401f907a3d6629ab4e69; buvid_fp=7bc8ecec0e75401f907a3d6629ab4e69; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTkyNjg2MTMsImlhdCI6MTcxOTAwOTM1MywicGx0IjotMX0.-LdByVQmu-_jQFzpGDFqMQcqNBAarAowkZWJgTFfta0; bili_ticket_expires=1719268553; SESSDATA=a78c20de%2C1734696255%2Cb4d7d%2A62CjAlG5VbsUom3wUMggQRRW4gH-Dla6slK6SjWQ0o0NWZYcL4vZeHnmode7f2aL38tDYSVnVBRXoyWVM3S0xQWFVJbUc5TzMxMWlBaFdNRkEtY0JSSHgzeFhJTlhPaDhwX0htdHJjU3NDMnRnTGVIc1d0eWxwUE5rVWtTZEpnMHJUZ1dRanI5NnhBIIEC; bili_jct=c4704f6d7e6253cd5671c1d19e2d9cc0; sid=84sbggfc; home_feed_column=5; browser_resolution=1707-940; CURRENT_QUALITY=80; bp_t_offset_37424969=946595446120251392; b_lsid=B6BAF423_1904AA658CD; bsource=search_google"
}

# Function to get replies with dynamic wts
def get_replies(wts):
    api_url = f"https://api.bilibili.com/x/v2/reply/wbi/main?oid=1005894049&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=f2902c30d9a3e44d117cb18e068db066&wts={wts}"
    return fetch_comments(api_url, headers, cookies)

# Fetch initial replies
initial_replies = get_replies(1719258514)
print(json.dumps(initial_replies, indent=4))

# Experiment with different wts values
for wts in range(1719257656, 1719258514, 10):  # Try different values in range
    replies = get_replies(wts)
    if replies:
        print(f"wts={wts}: {len(replies['data']['replies']) if 'data' in replies and 'replies' in replies['data'] else 0} replies")
