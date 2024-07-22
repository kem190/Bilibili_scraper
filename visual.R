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

df_raw <- read_csv('C:\\Users\\57016\\PycharmProjects\\All_about_social_mentality_online\\pachong\\comment_data_3_0705.csv')

df <- read_csv('C:\\Users\\57016\\PycharmProjects\\All_about_social_mentality_online\\pachong\\comment_data_3_0705.csv')
df_sna <- read.csv('weighted_edgelist.csv')
df <- as.data.table(df)
df_sna <- as.data.table(df_sna)
df_sna <- df_sna %>%
  rename(name = Name)
df <- df %>%
  rename(name = title)
colnames(df)
head(df_sna)
nnnnnams <- table(unique(df$oid))
merged_df = merge(df, df_sna, by='name')

no_text_df <- merged_df %>%
  select(name, author, username, sex, location, likes, time, Community) %>%
  rename(community = Community)

#save(no_text_df, file = 'no_text_df.R')

loc <- as.data.table(table(no_text_df$location))

###################### map visual #####
library(ggplot2)
library(sf)
library(dplyr)
library(viridis) # For color scales
library(mapchina)
head(china)
View(china)

cured_china <- st_make_valid(china)

china_provinces_sf <- cured_china %>%
  group_by(Name_Province) %>%
  summarise(geometry = st_union(geometry),
            Pop_2010_sum = sum(Pop_2010, na.rm = TRUE))

china_provinces_sf <- china_provinces_sf %>%
  mutate(location = substr(Name_Province, 1,2))

loc <- loc %>%
  mutate(location = substr(V1, 1,2))

View(china_provinces_sf)

province_data_merged <- china_provinces_sf %>%
  left_join(loc, by = c("location" = "location"))

province_data_merged <- province_data_merged %>%
  mutate(percentage = N/Pop_2010_sum) %>%
  mutate(point_on_surface = st_point_on_surface(geometry))

province_data_merged <- province_data_merged %>%
  drop_na(percentage) %>%
  mutate(percentage_new = sprintf("%.2f", percentage * 100))

ggplot(data = province_data_merged) +
  geom_sf(aes(fill = N)) +
  scale_fill_gradientn(colors = c("white", "pink", "red"), na.value = "grey50") +
  geom_sf_text(aes(label = N), size = 3, color = "black") + # Add numbers
  theme_minimal() +
  labs(fill = "Value",
       title = "Heat Map of Values by Province",
       caption = "Source: Your Data Source")
library(ggrepel)
ggplot(data = province_data_merged) +
  geom_sf(aes(fill = percentage)) +
  geom_sf_text(aes(label = N, geometry = point_on_surface), size = 3, color = "black") +
  scale_fill_gradientn(colors = c("white", "pink", "red"), na.value = "grey50") +
  theme_minimal() +
  labs(fill = "评论占人口比例",
       title = "视频评论热力图",
       caption = "注：图中数字为评论绝对数量，热力图为评论占人口比例")

########## 统计描述 #############
library(scales)
library(tidyr)
no_text_df <- no_text_df %>%
  group_by(name) %>%
  mutate(comment_num = n())


no_text_df <- no_text_df %>%
  arrange(desc(comment_num))

no_text_df <- no_text_df %>%
  filter(comment_num <= 8500)

View(no_text_df)

no_text_df <- no_text_df %>%
  mutate(comment_num_group = cut(comment_num, breaks = seq(0, 5500, by = 200), include.lowest = TRUE, right = FALSE)) %>%
  drop_na()

ggplot(data = no_text_df, aes(x = comment_num_group)) +
  geom_histogram(stat = "count", fill = "blue", color = "black") +
  theme_minimal() +
  labs(title = '评论量分布', x = '评论数量区间', y = '视频数量') +
  scale_x_discrete(labels = function(x) {
    x <- gsub("\\[|\\]|\\(|\\)", "", x)  # Remove brackets
    x <- gsub(",", "-", x)  # Replace commas with dashes for range formatting
    x
  }) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

table(no_text_df$sex)

####### processing for further grouped analysis ##############
head(df)

table(is.na(no_text_df$community))
titles_list <- as.list(unique(no_text_df$name))

keywords <- c("姜萍", "数学")

# 将关键词列表组合成正则表达式模式
pattern <- paste(keywords, collapse = "|")

# 过滤掉包含任何关键词的行
selected_df <- no_text_df %>%
  filter(community <= 19)

titles_df <- selected_df %>%
  distinct(name, .keep_all = TRUE)

filtered_df <- titles_df %>%
  filter(!grepl(pattern, name))

peek <- filtered_df %>%
  filter(grepl("主", name))

original_counts <- titles_df %>%
  group_by(community) %>%
  summarise(count = n())

filtered_counts <- filtered_df %>%
  group_by(community) %>%
  summarise(count = n())

# 合并两个数据框进行比较
comparison <- original_counts %>%
  rename(original_count = count) %>%
  left_join(filtered_counts %>% rename(filtered_count = count), by = "community") %>%
  mutate(change = original_count - filtered_count) %>%
  mutate(change_per = change/original_count) %>%
  arrange(desc(change_per))

class(titles_list)
# 这里不得不人工看一眼community来判断这个数据的有效性了
sampled_df <- selected_df %>%
  group_by(community) %>%
  do(sample_n(., min(20, n()))) %>%
  ungroup() %>%
  select(name, community)

print(sampled_df)
trimmed_rel_data