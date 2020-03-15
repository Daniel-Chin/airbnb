import csv
import datetime
import os
from math import log, inf
from jdt import Jdt
from time import sleep

list_dir = os.listdir('../data/')
len_list_dir = len(list_dir)

def validate():
  one_day = datetime.timedelta(1)
  list_dir = os.listdir('../data/')
  len_list_dir = len(list_dir)
  for i, filename in enumerate(list_dir):
    if i % 8 == 0:
      print(i / len_list_dir)
    last_date = None
    with open('../data/' + filename, 'r') as f:
      c = csv.reader(f)
      assert next(c) == ['listing_id', 'date', 'available', 'price', 'adjusted_price', 'minimum_nights', 'maximum_nights']
      for line in c:
        str_date = line[1]
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
        if last_date is not None:
          assert date - last_date == one_day
        last_date = date
  print('ok')

def lossFile(id, x, which_end):
  with open(f'../data/{id}.csv', 'r') as f:
    c = csv.reader(f)
    next(c)
    availables = [1 if line[2] == 't' else 0 for line in c]
  if which_end == -1:
    availables = [*reversed(availables)]
  ground_truth, availables = availables[0], availables[1:x+1]
  if len(availables) < x:
    print('\nid', id, 'len', len(availables))
  acc = 0
  acc_weight = 0
  for i, value in enumerate(availables):
    if i > 6.4:
      weight = 1 - i / x
      acc += value * weight
      acc_weight += weight
  acc /= acc_weight
  try:
    if ground_truth:
      return -log(acc)
    else:
      return -log(1 - acc)
  except ValueError:  # log(0)
    # if x > 10:
    #   print('\nx=', x, 'log(0)! id=', id)
    return 5

def overallLoss(x, which_end, msg = ''):
  jdt = Jdt(len_list_dir, msg=msg, UPP=128)
  acc = 0
  for filename in list_dir:
    jdt.acc()
    acc += lossFile(filename.split('.')[0], x, which_end)
  jdt.complete()
  with open('x1x2_result_2.csv', 'a') as f:
    print(x, which_end, acc / len_list_dir, sep = ',', file = f)
  return acc

class Walker:
  def __init__(self, f, initial_x, initial_step, params = [], boundary = None):
    self.f = f
    self.x = initial_x
    self.step = initial_step
    self.y = inf
    self.params = params
    self.boundary = boundary
    self.stopped = False
  
  def do(self):
    if self.stopped: return
    new_x = self.x + self.step
    new_y = self.f(new_x, *self.params)
    if new_y < self.f:
      self.x = new_x
      self.y = new_y
      self.step *= 1.1
      if self.boundary is not None:
        if self.x < self.boundary[0] or self.x > self.boundary[1]:
          self.stopped = True
    else:
      self.step *= -.6

def main():
  for i in range(46, 300):
    overallLoss(i, 1, str(i))
    overallLoss(i, -1)

main()
