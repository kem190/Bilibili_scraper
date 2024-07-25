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
df <- df_raw
df <- read_csv('C:\\Users\\57016\\PycharmProjects\\All_about_social_mentality_online\\pachong\\comment_data_3_0705.csv')
df <- df %>%
  mutate(index = row_number())

############## 寻找跟姜萍直接相关的视频和评论 #########

df_jp <- df %>%
  filter(grepl("姜萍", text))
title_jp <- df %>%
  filter(grepl("姜萍", title))
titles <- c(df_jp$title, title_jp$title)

jp_rel_comments <- df %>%
  filter(title %in% titles)

write.csv(jp_rel_comments, file = "jp_rel_comments.csv")

############### cleaning and tokenising ############

# 删除系统生成的评论
jp_rel_comments <- read.csv("jp_rel_comments.csv")

# 删除只有表情的评论
clean_rel <- title_jp %>%
  mutate(text = gsub("\\[.*?\\]", "", text)) %>%
  mutate(text = str_replace_all(text, "@.*", "")) %>%
  mutate(text = str_replace_all(text, "https?://\\S+\\s*", "")) %>%
  mutate(text = trimws(text)) %>%  # Trim leading/trailing white spaces
  filter(text != "") %>%  # Remove empty strings
  filter(str_count(text, "[\u4e00-\u9fff]") > 2)
  drop_na(text)  # Drop NA values

peek <- clean_rel %>%
  group_by(title) %>%
  mutate(tit_count = n()) %>%
  arrange(!desc(tit_count)) %>%
  ungroup()

peek <- as.data.frame(table(clean_rel$title))
### peek ###
df_repetitive <- clean_rel %>%
  group_by(text) %>%
  filter(n() > 1) %>%
  select(text)
  ungroup()

########## tokenising  #############
jieba = worker()
  
jieba$bylines = TRUE
df <- clean_rel
df <- df %>%
  mutate(tokens = segment(text, jieba))
  
  
custom_stopwords <- readLines("cn_stopwords.txt")
remove_custom_stopwords <- function(tokens, stopwords) {
  tokens <- tokens[!tokens %in% stopwords]
  return(tokens)
}
  
  
  #df$clean_text_bag <- sapply(df$tokens, remove_custom_stopwords, stopwords = custom_stopwords)
  # Assuming df$tokens is a list of tokenized words for each document
df$clean_text_bag <- lapply(df$tokens, remove_custom_stopwords, stopwords = custom_stopwords)
df$clean_text_bag <- sapply(df$clean_text_bag, paste, collapse = " ")
  
df <- df %>%
  select(!tokens)
class(df$clean_text_bag)
  
write.csv(df, file = 'tokenised_rel_comments.csv')
write.csv(jp_rel_comments, file = "jp_rel_comments.csv")

########### 区分地区 ########
library(mapchina)
china_provinces <- china %>%
  as.data.frame() %>%
  mutate(location = substr(Name_Province, 1,2)) %>%
  select(Code_Province, location) %>%
  distinct(location, .keep_all = TRUE)

loc_rel <- df %>%
  mutate(location = substr(location, 1,2)) %>%
  left_join(china_provinces, by = 'location')%>%
  mutate(
    loc_1 = case_when(
      location %in% c("未知", "unknown") ~ location,
      is.na(Code_Province) ~ "海外",
      TRUE ~ as.character(location)
    )
  )


########### SNA
title_jp <- df %>%
  filter(grepl("姜萍", title))

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

loc <- as.data.table(table(jp_rel_comments$location))

###################### map visual #####
library(ggplot2)
library(sf)
library(dplyr)
library(viridis) # For color scales
library(mapchina)
library(tidyverse)
head(china)
View(china)

china_loc <- china$Name_Province
china_loc <- as.data.frame(china_loc)
china_loc <- china_loc %>%
  mutate(location = substr(china_loc, 1,2))
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

table(jp_rel_comments$sex)

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

peek <- jp_rel_vids %>%
  filter(grepl("主=", title))

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
selected_df <- df %>%
  distinct(name, .keep_all = TRUE)
sampled_df <- selected_df %>%
  group_by(Community) %>%
  do(sample_n(., min(20, n()))) %>%
  ungroup() %>%
  select(name, Community)

print(sampled_df)
trimmed_rel_data