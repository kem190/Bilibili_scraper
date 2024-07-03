import pandas as pd
from collections import Counter

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_colwidth', None)  # Show full column width
pd.set_option('display.expand_frame_repr', False)  # Prevent truncation
pd.set_option('display.float_format', '{:.10f}'.format)
def convert_play_value(value):
    if '万' in value:
        value = value.replace('万', '')
        return str(int(float(value) * 10000))
    return value

df = pd.read_csv('C:\\Users\\57016\\PycharmProjects\\All_about_social_mentality_online\\pachong\\related_video_data_3_new.csv')

df['play'] = df['play'].apply(convert_play_value)
df['meta_playbacks'] = df['meta_playbacks'].apply(convert_play_value)
# Counting occurrences of each pair
pair_counts = Counter(zip(df['meta_url'], df['url']))

# Converting the counts to a DataFrame
edge_list_df = pd.DataFrame(pair_counts.items(), columns=['Pair', 'Count'])
edge_list_df[['meta_url', 'url']] = pd.DataFrame(edge_list_df['Pair'].tolist(), index=edge_list_df.index)

# Dropping the Pair column
edge_list_df = edge_list_df.drop(columns=['Pair'])

# Adding the descriptive columns
meta_titles = df.drop_duplicates(subset=['meta_url'])[['meta_url', 'meta_title', 'meta_playbacks']]
url_titles = df.drop_duplicates(subset=['url'])[['url', 'title', 'play']]

# Merging the titles and play data with the edge list
edge_list_with_titles = edge_list_df.merge(meta_titles, on='meta_url', how='left').merge(url_titles, on='url', how='left')

if edge_list_with_titles['Count'].dtype == 'object':
    edge_list_with_titles['Count'] = pd.to_numeric(edge_list_with_titles['Count'], errors='coerce')

print(type(edge_list_with_titles['Count']))
print(edge_list_with_titles['Count'].dtype)
non_numeric_counts = edge_list_with_titles['Count'].isna().sum()
sorted = edge_list_with_titles.sort_values(by = 'Count', ascending=False)

print(sorted)
