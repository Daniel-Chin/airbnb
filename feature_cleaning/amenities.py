import csv
from collections import Counter

def main():
  with open('../data2/pilot_features.csv', 'r', encoding='utf-8') as f:
    c = csv.reader(f)
    head = next(c)
    col = head.index('amenities')
    all_amens = Counter()
    i = 0
    for row in c:
      i += 1
      if i & 16 == 0:
        print(i)
      amens = row[col]
      all_amens.update(amens[1:-1].split(','))
  [print(*x, sep='\t') for x in all_amens.most_common()]
  from console import console
  console(locals())

main()
