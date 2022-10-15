
import dk_scrape
import implied_probability
import csv
import ast
import operator



test = dk_scrape.NFLScraper()
myprops = test.nfl_props_dk()
writer = csv.writer(open("output/dk/test.csv", 'w'))
for k, v in myprops.items():  
  #print([k], [v])
  writer.writerow([[k], [v]])



player_prop = {}
with open("output/dk/test.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    player_prop[row[0]] = row[1]

#print(player_prop)

writer = csv.writer(open("output/dk/prob.csv", 'w'))    
for key, props in player_prop.items():
  update = ast.literal_eval(props)
  for prop in update:
    for k, v in prop.items():
      #print(v)
      for i,j in v.items():
        #print(j)
        #print(key, [k + i, j[0], convert(j[1])])
        writer.writerow([key, [k + i, j[0], implied_probability.convert(j[1])]])
        

checklist = []
with open("output/dk/prob.csv", 'r') as file: 
  csvreader = csv.reader(file)
  for row in csvreader:
    new = ast.literal_eval(row[1])
    checklist.append([new[2], '{} {} {}'.format(row[0], new[0], str(new[1]))])

header = ["Implied Probability", "Player-Prop"]
writer = csv.writer(open("output/dk/sorted_prob.csv", 'w')) 
writer.writerow(header)   
for i in sorted(checklist, reverse=True):
  writer.writerow(i)
  
  