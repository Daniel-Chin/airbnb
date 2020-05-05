library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.summary.rda')
popular.terms <- filter(ok.terms,n > 3000)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.2
))

library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.space.rda')
popular.terms <- filter(ok.terms,n > 3000)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.1
))

library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.description.rda')
popular.terms <- filter(ok.terms,n > 3000)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.1
))

library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.interaction.rda')
popular.terms <- filter(ok.terms,n > 1000)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.1
))

library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.host_about.rda')
popular.terms <- filter(ok.terms,n > 2000)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.1
))

library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.transit.rda')
popular.terms <- filter(ok.terms,n > 2000)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.1
))

library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.house_rules.rda')
popular.terms <- filter(ok.terms,n > 2400)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.1
))

