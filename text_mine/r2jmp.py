import csv
from jdt import Jdt

jobs = [
  'summary', 
  'space', 
  'description', 
  'interaction', 
  'host_about', 
  'transit', 
  'house_rules', 
]
N_JOBS = len(jobs)

def main():
  sentiCs = []
  topicCs = []
  all_files = []
  for job in jobs:
    f = open(f'sent_df.{job}.csv', 'r')
    all_files.append(f)
    c = csv.reader(f)
    sentiCs.append(c)
    next(c)
    f = open(f'output.{job}.csv', 'r')
    all_files.append(f)
    c = csv.reader(f)
    topicCs.append(c)
    next(c)
  with open('advanced.csv', 'w+', newline='') as f:
    cout = csv.writer(f)
    outHead = [f'polarity_{x}' for x in jobs]
    for job in jobs:
      for i in range(1, 21):
        outHead.append(f'topic_{job}_{i}')
    cout.writerow(outHead + ['doc_id'])
    with Jdt(51094, UPP = 128) as jdt:
      for x in zip(*sentiCs, *topicCs):
        jdt.acc()
        senti = x[:N_JOBS]
        topic = x[N_JOBS:]
        builder = []
        doc_id = senti[0][2]
        for sen in senti:
          builder.append(sen[1])
          assert doc_id == sen[2]
        for top in topic:
          print(top[0], doc_id)
          assert top[0] == doc_id
          builder.extend(top[1:21])
    [x.close() for x in all_files]

main()
