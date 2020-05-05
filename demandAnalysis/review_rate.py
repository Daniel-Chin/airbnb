import csv
import datetime
from jdt import Jdt
from calendarEstimate import X1

AVG_LENGTH = 6.4

def getAllId():
  import pickle
  with open('../data2/all_id.pickle', 'rb') as f:
    return pickle.load(f)

def main():
  with open('../raw/listings.csv', 'r', encoding='utf-8') as listingF:
    listingC = csv.reader(listingF)
    next(listingC)
    with open('../data2/calendar_estimate.csv', 'r') as estimateF:
      estimateC = csv.reader(estimateF)
      next(estimateC)
      with open('../data2/review_rate_regression.csv', 'w+', newline='') as outF:
        out = csv.writer(outF)
        out.writerow([
          'id', 'is_review_recent_z_score', 'reviews_per_month', 
          *[f'y_{x}' for x in X1], 
          'length_of_stay', 
        ])
        scrape_day = datetime.datetime.strptime('2/12/2020', '%m/%d/%Y')
        with Jdt(len(getAllId()), UPP = 16) as j:
          for id2, _, *estimate_line in estimateC:
            j.acc()
            while True:
              line = next(listingC)
              id = line[0]
              if id == id2:
                break
            else:
              raise Exception('error 328')
            min_nights, _, last_review, rpm = line[10:14]
            occupancy = estimate_line[len(X1):]
            length_of_stay = max(int(min_nights), AVG_LENGTH)
            y = [float(x) / length_of_stay for x in occupancy]
            if last_review == '':
              z_score = 999
            else:
              date = datetime.datetime.strptime(last_review, '%Y-%m-%d')
              blank = (scrape_day - date).days
              if blank < 3:
                z_score = 0
              else:
                z_score = blank / ((365.25 / 12) / float(rpm))
            out.writerow([id, z_score, rpm, *y, length_of_stay])
  print('ok')

main()
