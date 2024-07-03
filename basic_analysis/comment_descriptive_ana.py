import pandas as pd
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_colwidth', None)  # Show full column width
pd.set_option('display.expand_frame_repr', False)  # Prevent truncation


df = pd.read_csv('C:\\Users\\57016\\PycharmProjects\\All_about_social_mentality_online\\pachong\\comments_2.csv')
print(df.shape)

df['count'] = df.groupby('title')['title'].transform('count')

print(df)
print(df.shape)



