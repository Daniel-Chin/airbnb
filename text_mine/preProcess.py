import csv
from uuid import uuid4
from jdt import Jdt

name = 'name'
summary = 'summary'
space = 'space'
description = 'description'
interaction = 'interaction'
host_about = 'host_about'
neighborhood_overview = 'neighborhood_overview'
transit = 'transit'
house_rules = 'house_rules'
all_text = [
  name, 
  summary,
  space,
  description,
  interaction,
  host_about,
  neighborhood_overview,
  transit,
  house_rules,
]
need_word_count = [
  name, 
  summary,
  space,
  description,
  interaction,
  host_about,
  neighborhood_overview,
]

def wc(x):
  return x + '_word_count'

def main():
  with open('../raw/listings_details.csv', 'r', encoding='utf-8') as fin:
    cin = csv.reader(fin)
    header_in = next(cin)
    header_in_dict = {x:header_in.index(x) for x in all_text}
    header_in_dict['id'] = header_in.index('id')
    def lookup(row, x):
      return row[header_in_dict[x]]
    with open('./text.csv', 'w+', newline = '', encoding='utf-8') as fout:
      cout = csv.writer(fout)
      header_out = [
        'id', *all_text, 
        *[wc(x) for x in need_word_count], 
        'name_is_all_cap', 'name_avg_word_len', 'doc_id', 
      ]
      cout.writerow(header_out)
      with Jdt(50000, UPP=128) as jdt:
        for row in cin:
          jdt.acc()
          handle(row, cout, lookup)

def handle(row, cout, lookup):
  result = [lookup(row, 'id')] # id
  for x in all_text:
    result.append(lookup(row, x))
  for x in need_word_count:
    result.append(len(parse(lookup(row, x))))
  name = lookup(row, 'name')
  if name.upper() == name:
    result.append(1)
  else:
    result.append(0)
  words = parse(name)
  try:
    result.append(sum([len(x) for x in words]) / len(words))
  except ZeroDivisionError: 
    result.append('')
  result.append(uuid4())
  cout.writerow(result)

def parse(name):
  words = [x.strip(',.!?:;\'"()[]%&-') for x in name.split(' ')]
  return [x for x in words if x]

main()
