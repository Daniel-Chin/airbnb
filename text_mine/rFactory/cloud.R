library(wordcloud)
par(mar=c(0,0,0,0))
load('ok.terms.__TARGET__.rda')
popular.terms <- filter(ok.terms,n > 3000)
lengths(popular.terms)[1]
wordcloud(popular.terms$Terms,popular.terms$n,colors=brewer.pal(8,"Dark2"),scale=c(
  3,.1
))
