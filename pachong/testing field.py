import pandas as pd

df = pd.read_csv('related_video_data_1.csv')
df_trim = df[['url', 'title', 'name', 'play', 'dm']]

unique_df = df_trim.drop_duplicates(subset=['url'])
unique_df.to_csv('all_vids_1.csv', index=False)
print(unique_df.shape)