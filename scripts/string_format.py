import csv

test = "['Quinnen Williams'] Sacksover 0.75"

test = test.replace('under',' Under')
test = test.replace('over',' Over')
print(test)

final = []

with open("output/dk/sorted_prob.csv", 'r') as file: 
  csvreader = csv.reader(file)
  for row in csvreader:
    for i in row:
      for word in i.split():
        word = word.replace('under',' Under')
        word = word.replace('over',' Over')
  
    
