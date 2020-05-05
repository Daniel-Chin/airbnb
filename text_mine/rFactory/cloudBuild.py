jobs = [
  'summary', 
  'space', 
  'description', 
  'interaction', 
  'host_about', 
  'transit', 
  'house_rules', 
]

def main():
  with open('cloud.R', 'r') as f:
    template = f.read()
  with open('../cloud_it.R', 'w+') as outF:
    for job in jobs:
      outF.write(template.replace('__TARGET__', job))
      outF.write('\n')

main()
