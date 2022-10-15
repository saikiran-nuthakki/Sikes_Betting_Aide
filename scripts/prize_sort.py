import csv

daily = {}

with open("output/prizepicks/single_sheet.csv", 'r') as file: 
  csvreader = csv.reader(file)
  for row in csvreader:
    if row[0] in daily:
      daily[row[0]] += [row[1], row[2]]
    else:
      daily[row[0]] = [row[1], row[2]]
      
print(daily.items())


