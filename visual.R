library(quanteda)
library(quanteda.textmodels)
library(stringr)
library(text2vec)
library(topicmodels)
library(tm)
library(quanteda.textplots)
library(readr)
library(data.table)
library(dplyr)
library(jiebaR)
library(tidytext)
library(tidytext)
library(reshape2)
library(ggplot2)
library(ggthemes)
library(readr)

df <- read_csv('C:\\Users\\57016\\PycharmProjects\\All_about_social_mentality_online\\pachong\\comment_data_3_0705.csv')
df <- read_csv('df_tokenized.csv')
metadata <- read.csv('pachong\\related_video_data_2_new.csv')
data_3 <- read.csv('pachong\\related_video_data_3_new.csv')
df_sna <- read.csv('weighted_edgelist.csv')
df <- as.data.table(df)
df_sna <- as.data.table(df_sna)
df_sna <- df_sna %>%
  rename(name = Name)
df <- df %>%
  rename(name = title)
colnames(df)
head(df_sna)

merged_df = merge(df, df_sna, by='name')

df <- merged_df

colnames(df)

no_text_df <- merged_df %>%
  select(name, author, username, sex, location, likes, time, Community) %>%
  rename(community = Community)

loc <- as.data.table(table(no_text_df$location))

## visual ##
library(ggplot2)
library(sf)
library(dplyr)
library(viridis) # For color scales
library(mapchina)
head(china)

china <- china
geo_data <- chine %>%
  group_by(Name_province)

st_write(china, "your/path/to/china.shp", layer_options = "ENCODING=UTF-8")

province_data_merged <- provinces_sf %>%
  left_join(province_data, by = c("province_name_column" = "province"))
