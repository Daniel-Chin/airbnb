# Topic Modeling
## load results (so you don't have to run the algorithm)
# load('lda.summary.rda')

# post.lda.summary <- posterior(lda.summary) #get the posterior probability of the topics for each document and of the terms for each topic

##  sum.lda
# sum.terms <- as.data.frame(post.lda.summary$terms) %>% #matrix topic * terms
#   mutate(topic=1:20) %>% #add a column
#   gather(term,p,-topic) %>% #gather makes wide table longer, key=term, value=p, columns=-topic (exclude the topic column)
#   group_by(topic) %>%
#   mutate(rnk=dense_rank(-p)) %>% #add a column
#   filter(rnk <= 10) %>%
#   arrange(topic,desc(p)) 

# sum.terms %>%
#   filter(topic==1) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 1') + theme(text=element_text(size=20))

# sum.terms %>%
#   filter(topic==2) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 2') + theme(text=element_text(size=20))

# sum.terms %>%
#   filter(topic==3) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 3') + theme(text=element_text(size=20))

# sum.terms %>%
#   filter(topic==8) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 8')

# sum.terms %>%
#   filter(topic==10) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip() + 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 10')

# sum.terms %>%
#   filter(topic==12) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 12')

# sum.terms %>%
#   filter(topic==18) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 18')

# sum.terms %>%
#   filter(topic==19) %>%
#   ggplot(aes(x=reorder(term,p),y=p)) + geom_bar(stat='identity') + coord_flip()+ 
#   xlab('Term')+ylab('Probability')+ggtitle('Topic 19')
