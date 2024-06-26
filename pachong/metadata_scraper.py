import requests
import json
import time
import random
import csv
from bs4 import BeautifulSoup


# Cookies (这是我自己的账号需要替换)
cookies = {
    "Cookies": "buvid3=E579EDE8-64A3-72D3-AD0D-9A111BE54DD103395infoc; b_nut=1713522703; CURRENT_FNVAL=4048; _uuid=A410CC8A5-FF13-FF86-D6FA-3542F4CC4910F05666infoc; buvid4=346F68FE-9DBC-DD3B-F9B3-C82EF884743305819-024041910-AYCtu957i4E2ZljBHTFxVg%3D%3D; rpdid=|(uJ~l)lmJ~R0J'u~uJlkk~ul; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NEW_POP; header_theme_version=CLOSE; buvid_fp_plain=undefined; DedeUserID=37424969; DedeUserID__ckMd5=02c3aef233c2afc9; PVID=1; fingerprint=7bc8ecec0e75401f907a3d6629ab4e69; buvid_fp=7bc8ecec0e75401f907a3d6629ab4e69; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTkyNjg2MTMsImlhdCI6MTcxOTAwOTM1MywicGx0IjotMX0.-LdByVQmu-_jQFzpGDFqMQcqNBAarAowkZWJgTFfta0; bili_ticket_expires=1719268553; SESSDATA=a78c20de%2C1734696255%2Cb4d7d%2A62CjAlG5VbsUom3wUMggQRRW4gH-Dla6slK6SjWQ0o0NWZYcL4vZeHnmode7f2aL38tDYSVnVBRXoyWVM3S0xQWFVJbUc5TzMxMWlBaFdNRkEtY0JSSHgzeFhJTlhPaDhwX0htdHJjU3NDMnRnTGVIc1d0eWxwUE5rVWtTZEpnMHJUZ1dRanI5NnhBIIEC; bili_jct=c4704f6d7e6253cd5671c1d19e2d9cc0; sid=84sbggfc; home_feed_column=5; browser_resolution=1707-940; CURRENT_QUALITY=80; bp_t_offset_37424969=946595446120251392; b_lsid=B6BAF423_1904AA658CD; bsource=search_google"
}

# URL生成

def generate_urls(base_url_first_page, base_url_with_offset, pages, step):
    urls = [base_url_first_page]  # Start with the first page without `o` parameter
    for page in range(2, pages + 1):
        offset = (page - 1) * step  # Adjust the offset calculation
        url = base_url_with_offset.format(page=page, offset=offset)
        urls.append(url)
    return urls

# Base URLs with and without the `o` parameter
base_url_first_page = "https://search.bilibili.com/all?vt=10787890&keyword=%E5%A7%9C%E8%90%8D&search_source=1&page=1"
base_url_with_offset = "https://search.bilibili.com/all?vt=10787890&keyword=%E5%A7%9C%E8%90%8D&search_source=1&page={page}&o={offset}"

# Number of pages to scrape
total_pages = 28

# Step for the offset parameter
offset_step = 36

# Generate the URLs
# urls = generate_urls(base_url_first_page, base_url_with_offset, total_pages, offset_step)
urls = "https://search.bilibili.com/all?vt=10787890&keyword=%E5%A7%9C%E8%90%8D&search_source=1&order=click&page=2&o=36"

# 准备工作
# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive"
}

# Open a CSV file to write the data
with open('bilibili_videos.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'URL', 'Author', 'Date', 'Playbacks', 'Flash_comments', 'Duration'])

    for url in urls:
        # Introduce random sleep interval between requests
        time.sleep(random.uniform(1, 5))
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the elements containing the desired text
        video_cards = soup.find_all('div', class_='bili-video-card')

        for card in video_cards:
            # Extract the video URL
            link_tag = card.find('a', href=True)
            video_url = link_tag['href'] if link_tag and 'href' in link_tag.attrs else ''
            if video_url.startswith('//'):
                video_url = 'https:' + video_url

            # Extract the video title
            title_tag = card.find('h3', class_='bili-video-card__info--tit')
            video_title = title_tag['title'] if title_tag and 'title' in title_tag.attrs else ''

            # Extract the author
            author_tag = card.find('span', class_='bili-video-card__info--author')
            video_author = author_tag.text.strip() if author_tag else ''

            # Extract the date
            date_tag = card.find('span', class_='bili-video-card__info--date')
            video_date = date_tag.text.strip() if date_tag else ''

            # Extract playbacks and flash_comments
            stats_tags = card.find_all('span', class_='bili-video-card__stats--item')
            playbacks = stats_tags[0].text.strip() if len(stats_tags) > 0 else ''
            flash_comments = stats_tags[1].text.strip() if len(stats_tags) > 1 else ''

            # Extract duration
            duration_tag = card.find('span', class_='bili-video-card__stats--duration')
            video_duration = duration_tag.text.strip() if duration_tag else ''

            # Print the extracted information (optional)
            print(f'Title: {video_title}')
            print(f'URL: {video_url}')
            print(f'Author: {video_author}')
            print(f'Date: {video_date}')
            print(f'Playbacks: {playbacks}')
            print(f'Flash_comments: {flash_comments}')
            print(f'Duration: {video_duration}')
            print('----------')

            # Write the data to CSV
            writer.writerow([video_title, video_url, video_author, video_date, playbacks, flash_comments, video_duration])