import os
import pickle

def main():
  list_dir = [int(x.split('.')[0]) for x in os.listdir('data')]
  list_dir_mar = [int(x.split('.')[0]) for x in os.listdir('data_mar')]
  s = set(list_dir_mar)
  list_dir = [x for x in list_dir if x in s]
  list_dir.sort()
  with open('data2/all_id.pickle', 'wb+') as f:
    pickle.dump(list_dir, f)

main()
