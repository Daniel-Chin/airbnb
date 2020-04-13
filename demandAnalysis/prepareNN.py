import csv
from jdt import Jdt
import pickle

def largeChunks(id):
  with open(f'../data/{id}.csv', 'r') as f:
    c = csv.reader(f)
    next(c)
    availables = [1 if line[2] == 't' else 0 for line in c]
  result = [0, 0, 0, 0]
  sustain = 0
  availables.append(True)
  for a in availables:
    if not a: # unavailable
      sustain += 1
    else:
      if sustain > result[0]:
        result[0] = sustain
        result.sort()
      sustain = 0
  return reversed(result)

def main():
  with open('../data2/all_id.pickle', 'rb') as f:
    all_id = pickle.load(f)
  with Jdt(len(all_id), UPP = 128) as jdt:
    with open('../data2/large_chunks.csv', 'w+', newline='') as f:
      c = csv.writer(f)
      c.writerow([
        'id', 
        *[f'chunk_of_unavai_{x}' for x in range(4)], 
      ])
      for x in all_id:
        jdt.acc()
        c.writerow([x, *largeChunks(x)])

main()
