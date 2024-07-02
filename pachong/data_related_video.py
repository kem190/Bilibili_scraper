import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import time
import random
import traceback

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
metadata = pd.read_csv('all_data.csv')
metadata = metadata.drop_duplicates(subset=['url'])
date_execution = '2024/07/01'

# Set pandas display options to show all columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_colwidth', None)  # Show full column width
pd.set_option('display.expand_frame_repr', False)  # Prevent truncation

# Print the first 5 rows of the DataFrame
print(metadata.head())
print(metadata.shape)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

backoff_time = random.uniform(2, 5)

########################################

def extract_data(card, meta_url, meta_title, meta_author, meta_playbacks, meta_dm, meta_full_title, date_execution, oid):
    try:
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
            'meta_full_title': meta_full_title,
            'meta_author': meta_author,
            'meta_playbacks': meta_playbacks,
            'meta_dm': meta_dm,
            'url': f"https://www.bilibili.com/video/{vid}/",
            'oid': oid,
            'title': title,
            'name': name,
            'play': play,
            'dm': dm,
            'date_execution': date_execution
        }
    except Exception as e:
        print(f"Error extracting data: {e}")
        print(traceback.format_exc())
        return None

def make_request(url, headers, backoff_factor, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            else:
                print(f"Non-200 status code: {response.status_code} for URL: {url}")
                time.sleep(backoff_factor * (2 ** attempt))
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            print(traceback.format_exc())
            time.sleep(backoff_factor * (2 ** attempt))
    return None

def extract_aid(soup):
    script_tag = soup.find('script', string=re.compile(r'window\.__INITIAL_STATE__')).text.strip()
    if script_tag:
        aid_match = re.search(r'"aid":(\d+)', script_tag)
        if aid_match:
            return aid_match.group(1)
    return 'None'

all_video_data = []
error_indices = []
##第一次用的
#metadata.columns = ['meta_title', 'meta_url', 'meta_author', 'date', 'meta_playbacks', 'meta_dm', 'duration',
#                    'date_of_scraping']
# # 第二次
# metadata.columns = ['url', 'title', 'author', 'play', 'dm']
#metadata = metadata.reset_index(drop=True)
number_of_times = 0  # Initialize the counter

for index, row in metadata.iterrows():
    try:
        meta_url = row['url']
        meta_title = row['title']
        meta_author = row['author']
        meta_playbacks = row['play']
        meta_dm = row['dm']

        # Print the current row for debugging
        print(f"Processing index {index} with URL: {meta_url}")

        # Skip if URL is NaN or not properly formatted
        if pd.isna(meta_url) or not re.match(r'^https?://www.bilibili.com/video/', meta_url):
            print(f"Skipping invalid URL at index {index}: {meta_url}")
            continue

        response = make_request(meta_url, headers=headers, backoff_factor=backoff_time)
        sleep = random.uniform(0.5, 2.5)
        time.sleep(sleep)
        print(f'sleeping for {sleep}')
        soup = BeautifulSoup(response.content, 'html.parser')

        # extract oid
        oid = extract_aid(soup)

        # extract full title
        meta_full_title = soup.find('h1', class_='video-title special-text-indent')
        if meta_full_title:
            meta_full_title = meta_full_title.text.strip()
        else:
            print(f"Title tag not found in the HTML for URL: {meta_url}")
            meta_full_title = 'Unknown Title'
            print(f'title not fetched{index}')
            error_indices.append(index)

        # Extract first rec_vid as well as dumping metadata in <------- metadata is being written HERE!
        next_play_card = soup.find('div', class_='next-play')
        if next_play_card:
            first_video_data = extract_data(next_play_card, meta_url, meta_title, meta_author, meta_playbacks, meta_dm, meta_full_title, date_execution, oid)
            all_video_data.append(first_video_data)

        # Extract the rest of the video data from the rec-list section
        rec_list_section = soup.find('div', class_='rec-list')
        if rec_list_section:
            rec_list_cards = rec_list_section.find_all('div', class_='video-page-card-small')
            for card in rec_list_cards:
                rec_video_data = extract_data(card, meta_url, meta_title, meta_author, meta_playbacks, meta_dm, meta_full_title, date_execution, oid)
                all_video_data.append(rec_video_data)

        number_of_times += 1  # Increment the counter
        print(rec_video_data)
        print(f"Processed {number_of_times} items")

        if number_of_times % 1000 == 0:
                    temp_df = pd.DataFrame(all_video_data)
                    temp_df.to_csv(f'related_video_data_3_temp_{number_of_times}.csv', index=False)
                    print(f"Temporary data saved at iteration {number_of_times}")

    except Exception as e:
        print(f"Error processing index {index}: {e}")
        print(traceback.format_exc())
        error_indices.append(index)

# Convert the collected data into a pandas DataFrame
df = pd.DataFrame(all_video_data)

# Write the DataFrame to a CSV file
df.to_csv('related_video_data_3_new.csv', index=False)

if error_indices:
    error_df = pd.DataFrame(error_indices, columns=['error_index'])
    error_df.to_csv('error_indices.csv', index=False)
    print("Error indices have been written to error_indices.csv")

print("Data has been written to related_video_data_3.csv")
