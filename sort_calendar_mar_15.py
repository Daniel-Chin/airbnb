import csv
import datetime

def distribute():
  with open('raw/calendar_mar_15.csv', 'r') as f:
    now_id = None
    outF = None
    all_id = set()
    try:
      c = csv.reader(f)
      head = next(c)
      for line in c:
        id = line[0]
        if id != now_id:
          if int(id) % 16 == 0: print(id)
          now_id = id
          if outF is not None:
            outF.flush()
            outF.close()
          if id in all_id:
            outF = open('data_mar/' + id + '.csv', 'a', newline = '')
            out = csv.writer(outF)
          else:
            outF = open('data_mar/' + id + '.csv', 'w+', newline = '')
            out = csv.writer(outF)
            out.writerow(head)
            all_id.add(id)
        out.writerow(line)
    finally:
      if outF is not None:
        outF.close()

def check():
  import os
  list_dir = os.listdir('data_mar/')
  set_dir = set()
  for filename in list_dir:
    set_dir.add(filename.split('.')[0])
  del list_dir
  print('step 2')
  with open('raw/calendar_mar_15.csv', 'r') as f:
    c = csv.reader(f)
    next(c)
    for line in c:
      id = line[0]
      assert id in set_dir
  print('ok')

def sortFile(filename):
  with open('data_mar/' + filename, 'r') as f:
    c = csv.reader(f)
    head = next(c)
    list_dates = []
    dict_data = {}
    for line in c:
      str_date = line[1]
      date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
      list_dates.append(date)
      dict_data[date] = line
  list_dates.sort()
  with open('data_mar/' + filename, 'w', newline='') as f:
    c = csv.writer(f)
    c.writerow(head)
    for date in list_dates:
      c.writerow(dict_data[date])

def checkFileSort(filename):
  list_dates = []
  with open('data_mar/' + filename, 'r') as f:
    c = csv.reader(f)
    _ = next(c)
    for line in c:
      str_date = line[1]
      date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
      list_dates.append(date)
  assert sorted(list_dates) == list_dates

def checkAll():
  import os
  list_dir = os.listdir('data_mar/')
  len_list_dir = len(list_dir)
  for i, filename in enumerate(list_dir):
    checkFileSort(filename)
    if i % 8 == 0:
      print(i / len_list_dir)
  print('ok')

print('Will distribute calendar_mar_15.csv to ./data_mar/')
assert(input('Files could be overwritten. Type "YES" to go: ') == 'YES')
distribute()
