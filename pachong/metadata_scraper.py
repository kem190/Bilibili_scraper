import requests
import json
import time
import random
import csv
from bs4 import BeautifulSoup

# 信息填写
#cookies =
base_url_first_page = "https://search.bilibili.com/all?vt=10787890&keyword=%E5%A7%9C%E8%90%8D&search_source=1&page=1"
base_url_with_offset = "https://search.bilibili.com/all?vt=10787890&keyword=%E5%A7%9C%E8%90%8D&search_source=1&page={page}&o={offset}"

date_of_execution = "2024_06_26"
IP_of_scraper = "UK"

def generate_urls(base_url_first_page, base_url_with_offset, pages, step):
    urls = [base_url_first_page]  # Start with the first page without `o` parameter
    for page in range(2, pages + 1):
        offset = (page - 1) * step  # Adjust the offset calculation
        url = base_url_with_offset.format(page=page, offset=offset)
        urls.append(url)
    return urls

def extract_oid(soup):
    script_tag = soup.find('script', string=re.compile(r'window\.__INITIAL_STATE__')).text.strip()
    if script_tag:
        aid_match = re.search(r'"aid":(\d+)', script_tag)
        if aid_match:
            return aid_match.group(1)
    return 'None'

# Base URLs with and without the `o` parameter

# Number of pages to scrape
total_pages = 28

# Step for the offset parameter
offset_step = 36

# Generate the URLs
urls = generate_urls(base_url_first_page, base_url_with_offset, total_pages, offset_step)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
# Locate the elements containing the desired text


# Extract and print the desired information
with open(f'jiangping_metadata_{date_of_execution}.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'URL', 'Author', 'Date', 'Playbacks', 'Flash_comments', 'Duration', 'date_of_scraping'])

    for url in urls:
        # Get the response from the URL
        response = requests.get(url, headers=headers)
        time.sleep(random.uniform(1, 5))
        soup = BeautifulSoup(response.content, 'html.parser')
        video_cards = soup.find_all('div', class_='bili-video-card')
        oid = extract_oid(soup)


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

            duration_tag = card.find('span', class_='bili-video-card__stats__duration')
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

            writer.writerow([video_title, video_url, video_author, video_date, playbacks, flash_comments, video_duration, date_of_scraping])
