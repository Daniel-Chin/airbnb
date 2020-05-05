rm(list=ls())

raw <- read.csv("./text.csv", header=TRUE, sep=",", stringsAsFactors = F)
raw <- data.frame(doc_id=raw$doc_id, __TARGET__=raw$__TARGET__, stringsAsFactors = F)

corpus <- VCorpus(DataframeSource(
  data.frame(doc_id=raw$doc_id, text=raw$__TARGET__, stringsAsFactors = FALSE)
))

corpus <- tm_map(corpus, content_transformer(replace_non_ascii), replacement = "", remove.nonconverted = TRUE)
corpus <- tm_map(corpus, content_transformer(tolower)) 
corpus <- tm_map(corpus, content_transformer(replace_word_elongation))
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, stemDocument, language="english") 
corpus <- tm_map(corpus, stripWhitespace)

dtm <- DocumentTermMatrix(corpus)
rm(list = c('corpus'))
__TC__

ok.terms <- filter(term.count, n > 1000)
save(ok.terms, file = 'ok.terms.__TARGET__.rda')

dtm.lda98 <- removeSparseTerms(dtm, 0.98)
dtm.lda99 <- removeSparseTerms(dtm, 0.99)
dtm.lda994 <- removeSparseTerms(dtm, 0.994)
if (dtm.lda98$ncol > 500) {
  dtm.lda <- dtm.lda98
  print('sparse 0.98')
} else {
  if (dtm.lda99$ncol > 500) {
    dtm.lda <- dtm.lda99
    print('sparse 0.99')
  } else {
    dtm.lda <- dtm.lda994
    print('sparse 0.994')
  }
}
dtm.lda$ncol
rm(list = c('dtm.lda98', 'dtm.lda99', 'dtm.lda994'))
dtm.lda <- dtm.lda[row_sums(dtm.lda) > 0,]

lda.result <- LDA(dtm.lda,k=20,method="Gibbs",
               control = list(seed = 2011, burnin = 1000,
                              thin = 100, iter = 5000))
save(lda.result,file='lda.__TARGET__.rda')

post.lda <- posterior(lda.result)

sum.terms <- as.data.frame(post.lda$terms) %>%
  mutate(topic=1:20) %>%
  gather(term,p,-topic) %>%
  group_by(topic) %>%
  mutate(rnk=dense_rank(-p)) %>%
  filter(rnk <= 10) %>%
  arrange(topic,desc(p)) 

write.csv(sum.terms, file="sum.terms.__TARGET__.csv")

topic.df <-post.lda$topics
write.csv(topic.df, file="output.__TARGET__.csv")
