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
df <- read.csv('df_tokenized.csv')
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
#df <- df %>% 
#  filter(Community <= 4) # 这里从909变成446，filter掉一半


jieba = worker()
jieba$bylines = TRUE
df <- df %>%
  mutate(tokens = segment(text_bag, jieba))


custom_stopwords <- readLines("cn_stopwords.txt")
remove_custom_stopwords <- function(tokens, stopwords) {
  tokens <- tokens[!tokens %in% stopwords]
  return(tokens)
}


df$clean_text_bag <- sapply(df$tokens, remove_custom_stopwords, stopwords = custom_stopwords)
# Assuming df$tokens is a list of tokenized words for each document
df$clean_text_bag <- lapply(df$tokens, remove_custom_stopwords, stopwords = custom_stopwords)

class(df$clean_text_bag)



################### topic modelling ############################
group_rep <- rep(df$Community, sapply(df$clean_text_bag, length))

# Create the data frame
df_token_group <- data.frame(
  token = unlist(df$clean_text_bag),
  group = group_rep
)


class(df_token_group$token)
token_freq_by_group <- df_token_group %>%
  group_by(group, token) %>%
  summarise(freq = n()) %>%
  arrange(group, desc(freq))


dtm_jieba <- token_freq_by_group %>%
  cast_dtm(group, token, freq)
tm::inspect(dtm_jieba)

library(ldatuning)
result <- FindTopicsNumber(
  dtm_jieba,
  topics = seq(from = 2, to = 50, by = 1),
  metrics = "CaoJuan2009",
  method = "Gibbs",
  control = list(seed = 19L),
  mc.cores = 12L, # LOOK AT MY LAPTOP!
  verbose = TRUE
)

FindTopicsNumber_plot(result)

lda_final <- LDA(dtm_jieba, k = 8, method = "Gibbs", control = list(seed = 19L))
topics_20 <- tidy(lda_final, matrix = "beta")
top_terms <- topics_20 %>%
  group_by(topic) %>%
  top_n(20, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)

print(top_terms)
options(scipen=10000)

top_terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free", ncol = 4) +
  scale_y_reordered() +
  scale_fill_grey(start = 0.35, end = 0.8) +
  theme_tufte(base_family = "sans")

# Plot
top_terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free", ncol = 3) +
  scale_y_reordered() +
  scale_fill_grey(start = 0.35, end = 0.8) +
  theme_tufte(base_family = "sans") +
  theme(
    text = element_text(size = 12),
    axis.text.y = element_text(angle = 0, hjust = 1),
    axis.text.x = element_text(angle = 90, hjust = 1),
    strip.text = element_text(size = 14),
    plot.margin = margin(10, 10, 10, 10)
  ) +
  labs(
    x = "Beta",
    y = "Term",
    title = "Top Terms in Each Topic"
  )

doc_topic_proportions <- posterior(lda_final)$topics
prevalence <- colMeans(doc_topic_proportions)
barplot(prevalence, main = "Prevalence of the topics", xlab = "topic number", ylab
        = "prevalence")

################### wordfish #########################
head(df)
df <- df %>% 
  filter(Community <= 19) # 这里从909变成683，filter掉25%，故意的
df$clean_text_bag <- sapply(df$clean_text_bag, paste, collapse = " ")
df_aggregated <- df %>%
  group_by(Community) %>%
  summarise(clean_text_bag = paste(clean_text_bag, collapse = " "))
corpus_data <- corpus(df_aggregated, text_field = "clean_text_bag", docid_field = "Community")

corpus <- corpus(df, text_field = "clean_text_bag", docid_field = "doc_index")

docvars(corpus, "Community") <- df$Community

docvars(corpus) <- df[, c("Community")]

tokens <- tokens(corpus_data, remove_punct = TRUE)

dfm <- dfm(tokens)
dfm <- dfm_trim(dfm, min_docfreq = 5, docfreq_type = "count")
dim(dfm)
# Run the Wordfish algorithm
wordfish_result <- textmodel_wordfish(dfm)

# Examine the results
summary(wordfish_result)
textplot_scale1d(wordfish_result)
textplot_scale1d(wordfish_result, margin = "features")

features <- wordfish_result[["features"]]

betas <- wordfish_result[["beta"]]

feat_betas <- as.data.frame(cbind(features, betas))
feat_betas$betas <- as.numeric(feat_betas$betas)

feat_betas %>%
  arrange(betas) %>%
  top_n(50)

top_features <- feat_betas %>%
  arrange(betas) %>%
  slice_head(n = 50)

print(top_features)

