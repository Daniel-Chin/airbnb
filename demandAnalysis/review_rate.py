import csv
import datetime
from jdt import Jdt

AVG_LENGTH = 6.4

def getAllId():
  import pickle
  with open('../data2/all_id.pickle', 'rb') as f:
    return pickle.load(f)

def main():
  with open('../raw/listings.csv', 'r', encoding='utf-8') as listingF:
    lisitngC = csv.reader(listingF)
    next(lisitngC)
    with open('../data2/calendar_estimate.csv', 'r') as estimateF:
      estimateC = csv.reader(estimateF)
      next(estimateC)
      with open('../data2/review_rate_regression.csv', 'w+', newline='') as outF:
        out = csv.writer(outF)
        out.writerow(['id', 'is_review_recent_z_score', 'reviews_per_month', 'y', 'occupancy_calendar', 'length_of_stay'])
        scrape_day = datetime.datetime.strptime('2/12/2020', '%m/%d/%Y')
        with Jdt(len(getAllId()), UPP = 64) as j:
          for line in lisitngC:
            j.acc()
            id = line[0]
            min_nights, _, last_review, rpm = line[10:14]
            id2, _, __, occupancy = next(estimateC)
            assert id == id2
            length_of_stay = max(int(min_nights), AVG_LENGTH)
            y = float(occupancy) / length_of_stay
            if last_review == '':
              z_score = 999
            else:
              date = datetime.datetime.strptime(last_review, '%Y-%m-%d')
              blank = (scrape_day - date).days
              z_score = blank / ((365.25 / 12) / float(rpm))
            out.writerow([id, z_score, rpm, y, occupancy, length_of_stay])
  print('ok')

main()
