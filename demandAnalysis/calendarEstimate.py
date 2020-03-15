import csv
from jdt import Jdt
import pickle

X1 = 6
X2 = 12

def predict(id, x, which_end):
  with open(f'../data/{id}.csv', 'r') as f:
    c = csv.reader(f)
    next(c)
    availables = [1 if line[2] == 't' else 0 for line in c]
  if which_end == -1:
    availables = [*reversed(availables)]
  availables = availables[:x]
  acc = 0
  acc_weight = 0
  for i, value in enumerate(availables):
    weight = 1 - i / x
    acc += value * weight
    acc_weight += weight
  acc /= acc_weight
  return acc

def oneListing(id, c):
  buffer = [id]
  probability_unavailable = 1 - predict(id, X1, 1)
  probability_closed = 1 - predict(id, X2, -1)
  buffer.append(probability_unavailable)
  buffer.append(probability_closed)
  buffer.append(probability_unavailable - probability_closed)
  c.writerow(buffer)

def main():
  with open('../data2/all_id.pickle', 'rb') as f:
    all_id = pickle.load(f)
  jdt = Jdt(len(all_id), UPP = 128)
  with open('../data2/calendar_estimate.csv', 'w', newline='') as f:
    c = csv.writer(f)
    c.writerow(['id', 'probability_unavailable', 'probability_closed', 'occupancy_rate'])
    [(oneListing(x, c), jdt.acc()) for x in all_id]
  jdt.complete()
  print('ok')

main()
