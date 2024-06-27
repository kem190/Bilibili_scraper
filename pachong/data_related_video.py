import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import time
import random

# 第一次循环，1xxx个视频
#metadata = pd.read_csv(
#    'C:/Users/57016/PycharmProjects/All_about_social_mentality_online/pachong/jiangping_metadata.csv')

# 第二次循环，4171个视频
# df = pd.read_csv('related_video_data_1.csv')
# df_trim = df[['url', 'title', 'name', 'play', 'dm']]
#
# unique_df = df_trim.drop_duplicates(subset=['url'])
# unique_df.to_csv('all_vids_1.csv', index=False)
# print(unique_df.shape)
metadata = pd.read_csv(
    'C:/Users/57016/PycharmProjects/All_about_social_mentality_online/pachong/all_vids_1.csv')
date_execution = '2024/06/27'

# Set pandas display options to show all columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_colwidth', None)  # Show full column width
pd.set_option('display.expand_frame_repr', False)  # Prevent truncation

# Print the first 5 rows of the DataFrame
print(metadata.head())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def extract_data(card, meta_url, meta_title, meta_author, meta_playbacks, meta_dm, date_execution):
    link_tag = card.find('a', href=True)
    video_id = link_tag['href'] if link_tag and 'href' in link_tag.attrs else ''
    vid = re.search(r'video/([A-Za-z0-9]+)', video_id).group(1)
    title = card.find('p', class_='title').text.strip()
    name = card.find('span', class_='name').text.strip()
    playinfo = list(card.find('div', class_='playinfo').stripped_strings)
    play = playinfo[0]
    dm = playinfo[1]

    return {
        'meta_url': meta_url,
        'meta_title': meta_title,
        'meta_author': meta_author,
        'meta_playbacks': meta_playbacks,
        'meta_dm': meta_dm,
        'url': f"https://www.bilibili.com/video/{vid}/",
        'title': title,
        'name': name,
        'play': play,
        'dm': dm,
        'date_execution': date_execution
    }


all_video_data = []
# 第一次用的
# metadata.columns = ['meta_title', 'meta_url', 'meta_author', 'date', 'meta_playbacks', 'meta_dm', 'duration',
#                     'date_of_scraping']
# 第二次
metadata.columns = ['meta_url', 'meta_title', 'meta_author', 'meta_playbacks', 'meta_dm']
metadata = metadata.reset_index(drop=True)
number_of_times = 0  # Initialize the counter

for index, row in metadata.iterrows():
    meta_url = row['meta_url']
    meta_title = row['meta_title']
    meta_author = row['meta_author']
    meta_playbacks = row['meta_playbacks']
    meta_dm = row['meta_dm']

    # Print the current row for debugging
    print(f"Processing index {index} with URL: {meta_url}")

    # Skip if URL is NaN or not properly formatted
    if pd.isna(meta_url) or not re.match(r'^https?://www.bilibili.com/video/', meta_url):
        print(f"Skipping invalid URL at index {index}: {meta_url}")
        continue

    response = requests.get(meta_url, headers=headers)
    time.sleep(random.uniform(1, 5))
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract first rec_vid
    next_play_card = soup.find('div', class_='next-play')
    if next_play_card:
        first_video_data = extract_data(next_play_card, meta_url, meta_title, meta_author, meta_playbacks, meta_dm, date_execution)
        all_video_data.append(first_video_data)

    # Extract the rest of the video data from the rec-list section
    rec_list_section = soup.find('div', class_='rec-list')
    if rec_list_section:
        rec_list_cards = rec_list_section.find_all('div', class_='video-page-card-small')
        for card in rec_list_cards:
            rec_video_data = extract_data(card, meta_url, meta_title, meta_author, meta_playbacks, meta_dm, date_execution)
            all_video_data.append(rec_video_data)

    number_of_times += 1  # Increment the counter
    print(f"Processed {number_of_times} items")

# Convert the collected data into a pandas DataFrame
df = pd.DataFrame(all_video_data)

# Write the DataFrame to a CSV file
df.to_csv('related_video_data_1.csv', index=False)

print("Data has been written to related_video_data_1.csv")
