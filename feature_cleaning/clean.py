import csv
from jdt import Jdt

ALL_AMEN = ['Wifi', 'Heating', 'Essentials', 'Kitchen', '"Smoke detector"', '"Air conditioning"', 'Hangers', '"Carbon monoxide detector"', 'TV', 'Shampoo', '"Hair dryer"', '"Laptop friendly workspace"', 'Iron', '"Hot water"', 'Refrigerator', '"Dishes and silverware"', 'Washer', 'Dryer', '"Fire extinguisher"', 'Microwave', '"Lock on bedroom door"', 'Stove', '"Cooking basics"', 'Oven', '"Free street parking"', '"Coffee maker"', '"First aid kit"', '"Bed linens"', 'Internet', 'Elevator']
LEN_ALL_AMEN = len(ALL_AMEN)
def amen(raw):
  result = ['f'] * LEN_ALL_AMEN
  for tag in raw[1:-1].split(','):
    try:
      pos = ALL_AMEN.index(tag)
      result[pos] = 't'
    except ValueError:
      continue
  return result

def rate(raw):
  if raw == 'N/A':
    return ''
  if not raw:
    return ''
  assert raw[-1] == '%'
  return str(
    int(raw[:-1]) * .01
  )

def verificaitons(raw):
  return str(len(raw.split("', '")))

MONTH = 365.25 / 12
def prices(price, weekly_price, monthly_price):
  price = float(price[1:])
  if weekly_price:
    weekly_price = float(weekly_price[1:])
    weekly_discount = (price - weekly_price / 7) / price
  else:
    weekly_discount = 0
  if monthly_price:
    monthly_price = float(monthly_price[1:])
    monthly_discount = (price - monthly_price / MONTH) / price
  else:
    monthly_discount = 0
  return [
    '$' + str(price), 
    str(weekly_discount), 
    str(monthly_discount), 
  ]

def main():
  with open('../data2/pilot_features.csv', 'r', encoding='utf-8') as f:
    c = csv.reader(f)
    head = next(c)
    with open('../data2/cleaned.csv', 'w+', encoding='utf-8', newline = '') as outF:
      out = csv.writer(outF)
      amen_col = head.index('amenities')
      rate_col = head.index('host_response_rate')
      veri_col = head.index('host_verifications')
      pric_col = head.index('weekly_price') - 1
      fill_0 = [head.index(x) for x in ['security_deposit', 'cleaning_fee']]
      fill_1 = [head.index(x) for x in ['host_listings_count', 'host_total_listings_count', 'bedrooms', 'beds']]
      outHead = head[:]
      outHead[veri_col] = 'num_of_host_verifications'
      outHead[pric_col+1] = 'weekly_discount'
      outHead[pric_col+2] = 'monthly_discount'
      out.writerow(outHead[:amen_col] + [
        'amen_' + x for x in ALL_AMEN
      ] + outHead[amen_col+1:])
      with Jdt(50000, 'cleaning', UPP=256) as jdt:
        for row in c:
          jdt.acc()
          try:
            row[rate_col] = rate(row[rate_col])
            row[rate_col + 1] = rate(row[rate_col + 1])
            row[veri_col] = verificaitons(row[veri_col])
            row[pric_col:pric_col+3] = prices(*row[pric_col:pric_col+3])
            for col in fill_0:
              if not row[col]:
                row[col] = '0'
            for col in fill_1:
              if not row[col]:
                row[col] = '1'
            row = row[:amen_col] + amen(row[amen_col]) + row[amen_col+1:]
            out.writerow(row)
          except:
            with open('error.log', 'a') as f:
              print(row[0], file=f)
              import traceback
              traceback.print_exc()

if __name__ == '__main__':
  main()
