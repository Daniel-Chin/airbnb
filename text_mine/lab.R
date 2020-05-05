# Built on the example script used in D3M

##############################################################
# Basics of Text Mining, D3M NYU Stern
# Exercises from Karsten Hansen, UCSD
##############################################################

# 1) Word frequency and word cloud
# 2) Sentiment
# 3) Topic models

##############################################################
rm(list=ls())
# install.packages("dplyr")
# install.packages("tidyr")
# install.packages("slam")
# install.packages("topicmodels")
# install.packages("wordcloud")
# install.packages("ggmap")
# install.packages("SnowballC")
# install.packages("tm")
# install.packages("textclean")

setwd("E:/ClassNote/D3M/airBnB/text_mine")

library(dplyr)
library(ggplot2)
library(tidyr)
library(ggmap)
library(cluster)
library(tm)
library(topicmodels)
library(slam)
library(SnowballC)
library(textclean)

#load data
raw <- read.csv("./text.csv", header=TRUE, sep=",", stringsAsFactors = F)

#########################################################################################
# 1) Word frequency and word cloud
## clean & Create DTM

# Corpus is a collection of text documents
# DTM: frequency of terms that occur in a collection of documents

# Read intro to TM Package https://cran.r-project.org/web/packages/tm/vignettes/tm.pdf
########################################################################################
summary.corpus <- VCorpus(VectorSource(
  data.frame(doc_id=raw$doc_id, text=raw$summary, stringsAsFactors = FALSE)
)) #Create volatile corpora
#transaformation of the corpora

summary.corpus.clean <- summary.corpus
#if the line above does not work and you use a MAC, try this
# summary.corpus.clean <- tm_map(summary.corpus, content_transformer(function(x) iconv(x, to='UTF-8', sub='byte')))
# review.corpus.clean <- tm_map(review.corpus.clean, content_transformer(tolower)) #Interface to apply transformation functions to corpora.
# summary.corpus.clean <- tm_map(summary.corpus.clean, replace_emoji)
summary.corpus.clean <- tm_map(summary.corpus.clean, replace_non_ascii, replacement = "", remove.nonconverted = TRUE)
summary.corpus.clean <- tm_map(summary.corpus.clean, PlainTextDocument)
summary.corpus.clean <- tm_map(summary.corpus.clean, content_transformer(tolower)) #Interface to apply transformation functions to corpora.
# summary.corpus.clean <- tm_map(summary.corpus.clean, replace_internet_slang)
summary.corpus.clean <- tm_map(summary.corpus.clean, replace_word_elongation)
summary.corpus.clean <- tm_map(summary.corpus.clean, removeWords, stopwords("english"))
summary.corpus.clean <- tm_map(summary.corpus.clean, removePunctuation)
summary.corpus.clean <- tm_map(summary.corpus.clean, removeNumbers)
summary.corpus.clean <- tm_map(summary.corpus.clean, stemDocument, language="english") #perform stemming which truncates words
summary.corpus.clean <- tm_map(summary.corpus.clean, stripWhitespace)

dtm <- DocumentTermMatrix(summary.corpus.clean)
inspect(dtm[1:10, c("clean")])

## Check frequency and make frequency plot
freq <- colSums(as.matrix(dtm))
freq[1:10]

#Very hard to see, so let's make a plot
term.count <- as.data.frame(as.table(dtm)) %>%
  group_by(Terms) %>%
  summarize(n=sum(Freq))
# 
# # Keep High Frequency words only
# term.count %>% 
#   filter(cume_dist(n) > 0.9996) %>% #cume_dist is the cumulative distribution function which gives the proportion of values less than or equal to the current rank
#   ggplot(aes(x=reorder(Terms,n),y=n)) + geom_bar(stat='identity') + 
#   coord_flip() + xlab('Counts') + ylab('')
# 
# #Another way to find the frequent terms 
# findFreqTerms(dtm, lowfreq=150)

 # find terms correlated with "room" 
# room <- data.frame(findAssocs(dtm, "room", .9))
# room %>%
#   add_rownames() %>%
#   ggplot(aes(x=reorder(rowname,room),y=room)) + geom_point(size=4) + 
#   coord_flip() + ylab('Correlation') + xlab('Term') + 
#   ggtitle('Terms correlated with Room') + theme(text=element_text(size=20))
# 
# bathroom <- data.frame(findAssocs(dtm, "bathroom", 0.99))
# bathroom %>%
#   add_rownames() %>%
#   ggplot(aes(x=reorder(rowname,bathroom),y=bathroom)) + geom_point(size=4) + 
#   coord_flip() + ylab('Correlation') + xlab('Term') + 
#   ggtitle('Terms correlated with Bathroom')

## Make wordcloud
# install.packages("wordcloud")
library(wordcloud)
ok.terms <- filter(term.count, n > 1000)
save(ok.terms, file = 'summary_ok.terms.rda')
# popular.terms <- filter(ok.terms,n > 5000)
# popular.terms
# par(mar=c(0,0,0,0))
# wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
#   3,.1
# ))

###########################################################################################
# 2) SENTIMENT ANALYSIS
# R package: "SentimentAnalysis"
###########################################################################################
# install.packages("SentimentAnalysis")
library(SentimentAnalysis)
t <- as.character(raw$summary)
summary_sentiment              <- analyzeSentiment(t[00001:10000])$SentimentQDAP
summary_sentiment[10001:20000] <- analyzeSentiment(t[10001:20000])$SentimentQDAP
summary_sentiment[20001:30000] <- analyzeSentiment(t[20001:30000])$SentimentQDAP
summary_sentiment[30001:40000] <- analyzeSentiment(t[30001:40000])$SentimentQDAP
summary_sentiment[40001:50000] <- analyzeSentiment(t[40001:50000])$SentimentQDAP
summary_sentiment[50001:51097] <- analyzeSentiment(t[50001:51097])$SentimentQDAP
#if the above line does not work and you have a MAC, try this
# recode <-function(x) {iconv(x, to='UTF-8-MAC', sub='byte')}
# sentiment <- analyzeSentiment(recode(aria.reviews$text))

sent_df = data.frame(polarity=summary_sentiment, business = raw, stringsAsFactors=FALSE)

# Plot results and check the correlation betweeen polarity and review stars
summary(sent_df$polarity)
sent_df %>% filter(is.na(polarity)==TRUE)%>%select(business.summary)
#correct for NA
sent_df$polarity[is.na(sent_df$polarity)]=0
write.csv(sent_df, file="sent_df.summary.csv")
# sent_df$business.stars<-as.numeric(sent_df$business.stars)
# sent_df %>%
#   group_by(business.stars) %>%
#   summarize(mean.polarity=mean(polarity,na.rm=TRUE)) %>%
#   ggplot(aes(x=business.stars,y=mean.polarity)) +  geom_bar(stat='identity',fill="blue") +  
#   ylab('Mean Polarity') + xlab('Stars')  + theme(text=element_text(size=20))
# cor(sent_df$polarity,sent_df$business.stars)

# Create helpful variable and plot by helpful
# sent_df$helpful[sent_df$business.votes.useful==0]<-"Not Helpful"
# sent_df$helpful[sent_df$business.votes.useful!=0]<-"Helpful"

# spineplot(as.factor(sent_df$helpful)~as.factor(sent_df$business.stars),col = c("red3", "grey", "green3"))

#Correlation between helpfulness and polarity
#change useful from factor to numeric
# sent_df$business.votes.useful=as.numeric(paste(sent_df$business.votes.useful))
#correlation between polarity and useful
# cor(sent_df$polarity,sent_df$business.votes.useful)

###########################################################################################
# 3) TOPIC MODELING
# R package: "topicmodels"
###########################################################################################

## set.up.dtm.for.lda.1
library(topicmodels)
library(slam)

dtm.lda <- removeSparseTerms(dtm, 0.98)
doc_id <- raw$doc_id[row_sums(dtm.lda) > 0]
dtm.lda <- dtm.lda[row_sums(dtm.lda) > 0,]

## run LDA algorithm - WARNING: takes a while to run!
lda.summary <- LDA(dtm.lda,k=20,method="Gibbs",
               control = list(seed = 2011, burnin = 1000,
                              thin = 100, iter = 5000))
save(lda.summary,file='lda.summary.rda')

## load results (so you don't have to run the algorithm)
# load('lda.summary.rda')

post.lda.summary <- posterior(lda.summary) #get the posterior probability of the topics for each document and of the terms for each topic

##  sum.lda
sum.terms <- as.data.frame(post.lda.summary$terms) %>% #matrix topic * terms
  mutate(topic=1:20) %>% #add a column
  gather(term,p,-topic) %>% #gather makes wide table longer, key=term, value=p, columns=-topic (exclude the topic column)
  group_by(topic) %>%
  mutate(rnk=dense_rank(-p)) %>% #add a column
  filter(rnk <= 10) %>%
  arrange(topic,desc(p)) 

sum.terms %>%
  filter(topic==1) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 1') + theme(text=element_text(size=20))

sum.terms %>%
  filter(topic==2) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 2') + theme(text=element_text(size=20))

sum.terms %>%
  filter(topic==3) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 3') + theme(text=element_text(size=20))

sum.terms %>%
  filter(topic==8) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 8')

sum.terms %>%
  filter(topic==10) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 10')

sum.terms %>%
  filter(topic==12) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 12')

sum.terms %>%
  filter(topic==18) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 18')

sum.terms %>%
  filter(topic==19) %>%
  ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
  xlab('Term')+ylab('Probability')+ggtitle('Topic 19')

write.csv(sum.terms, file="sum.terms.summary.csv")

# If you want to add topics as features for machine learning
# summary.subset <- raw[raw$doc_id %in% doc_id, c("doc_id")]
topic.df <-post.lda.summary$topics
# temp <- data.frame(post.lda.summary, topic.df)
# combined.df<-temp %>% select(-review_id)%>%group_by(business_id) %>%summarise_all(list(mean))
# Export the dataset to csv
write.csv(topic.df, file="output.summary.csv")
