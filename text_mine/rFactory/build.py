jobs = [
  'summary', 
  'space', 
  'description', 
  'interaction', 
  'host_about', 
  'transit', 
  'house_rules', 
]

def main():
  tc = termCount()
  with open('head.R', 'r') as f:
    head = f.read()
  with open('template.R', 'r') as f:
    template = f.read()
  with open('../do_it.R', 'w+') as outF:
    outF.write(head)
    outF.write('\n')
    for job in jobs:
      outF.write(template.replace('__TARGET__', job).replace('__TC__', tc))
      outF.write('\n')

def termCount():
    first = 'term.count <-                       as.data.frame(as.table(dtm[%s:%s, 1:dtm$ncol])) %%>%% group_by(Terms) %%>%% summarize(n=sum(Freq))'
    then = 'term.count <- bind_rows(term.count, as.data.frame(as.table(dtm[%s:%s, 1:dtm$ncol])) %%>%% group_by(Terms) %%>%% summarize(n=sum(Freq))) %%>%% group_by(Terms) %%>%% summarise_all(sum)'
    buffer = []
    for i in range(0, 50000, 2000):
        start = format(i + 1, '05')
        end = format(min(51097, i + 2000), '05')
        buffer.append((first if i == 0 else then) % (start, end))
    return '\n'.join(buffer)

main()
