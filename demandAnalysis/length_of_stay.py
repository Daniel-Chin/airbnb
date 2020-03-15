'''
Result: Adjusted avg: 1.031053909664887
So we cannot adjust like this.
This means minimum_nights are unbalanced in terms of sales. 
Higher minimum_nights listings have significantly lower sales.
'''
import csv

AVG = 6.4

def getAllId():
  import pickle
  with open('../data2/all_id.pickle', 'rb') as f:
    return pickle.load(f)

def main():
  acc = 0
  bdd = 0
  acc_nights = 0
  with open('../raw/listings.csv', 'r', encoding='utf-8') as f:
    c = csv.reader(f)
    next(c)
    for line in c:
      minimum_nights = int(line[10])
      if minimum_nights > AVG:
        acc += 1
        acc_nights += minimum_nights
      else:
        bdd += 1
  print('total:', acc + bdd)
  print('Adjusted avg:', (AVG * (acc + bdd) - acc_nights) / bdd)
  print('also total:', len(getAllId()))
  print(acc, bdd)

main()
