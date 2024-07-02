library(quanteda)
library(quanteda.textmodels)

library(readr)
library(data.table)
library(dplyr)
library(jiebaR)
library(tidytext)
library(tidytext)
df <- read.csv('df_tokenized.csv')
colnames(df)
head(df)

df <- df %>% 
  filter(count >= 10)

custom_stopwords <- readLines("cn_stopwords.txt")

df$clean_tokens <- lapply(df$text_bag, function(x) setdiff(x, STOPWORDS$word, ))


corpus <- corpus(df, text_field = "text_bag", docid_field = "doc_index")
docvars(corpus) <- df[, c("doc_index", "play")]

tokens <- tokens(corpus, remove_punct = TRUE)

dfm <- dfm(tokens)
dfm <- dfm_trim(dfm, min_docfreq = 5, docfreq_type = "count")
dim(dfm)
# Run the Wordfish algorithm
wordfish_result <- textmodel_wordfish(dfm)

# Examine the results
summary(wordfish_result)
doc_positions <- wordfish_result$docs
plot(doc_positions, main = "Document Positions", xlab = "Document Index", ylab = "Position", type = "h")

# Extract and plot word parameters
word_params <- wordfish_result$features
plot(word_params$beta, main = "Word Parameters", xlab = "Word Index", ylab = "Beta", type = "h")
