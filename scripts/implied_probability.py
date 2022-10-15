import ast
#converts decimal odds to implied probability

def convert(decimal_odds):
  conversion = round((1/decimal_odds) * 100, 5)
  return conversion

