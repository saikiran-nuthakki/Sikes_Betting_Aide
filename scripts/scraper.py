
import csv
import sys

import requests

from create_player_list import create_player_list
from create_stat_list import create_stat_list
from find import find
from find_league import find_league

# parse command line arguments
argument_length = len(sys.argv)

try: 
  league_string = sys.argv[1]
  league = find_league(sys.argv[1])
except IndexError:
  sys.exit('A league must be provided. See the README.md file for available leagues')

# determine stat to generate lines for (optional, needs further development)
if argument_length == 3:
  league = find_league(sys.argv[1])
  stat = sys.argv[2]

HEADERS = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
  'Dnt': ('1'),
  'cache-control': 'max-age=0',
  'Accept-Encoding': ('gzip, deflate, br'),
  'Accept': ('application/geo+json'),
  'Accept-Language': ('en'),
  'origin': ('https://app.prizepicks.com')
}

payload = {
  'league_id': league,
  'per_page': '1000',
  'single_stat': 'true',
}

# making the intial request
initial_request = requests.get('https://partner-api.prizepicks.com/projections', params=payload, headers=HEADERS, timeout=30)
# parsing the response json
pp_data = initial_request.json()

# creating list of players and stats availble for the request
player_list = create_player_list(pp_data['included'])
stat_list = create_stat_list(pp_data['included'])

# iterate over the stats that lines are set for
for stat in stat_list:
  # filter all of the returned data down to the current stat
  filtered_data = list(filter(lambda d: d['attributes']['stat_type'] == stat, pp_data['data']))
  # empty list for the lines for that stat
  lines = []

  # for each player in the filtered data, find the player's name from the
  # player list using the player_id, then create a dict for that line with the
  # player's name and line. Then append that line dict to the lines list
  for player in filtered_data: 
    player_id = player['relationships']['new_player']['data']['id']
    player_index = find(player_list, 'id', player_id)
    player_name = player_list[player_index]['name']
    line = {
      'player': player_name,
      'line': player['attributes']['line_score']
    }

    lines.append(line)

  # grab the keys for the csv file, then write the csv file to the output folder
  keys = lines[0].keys()
  with open('output/{0}_{1}.csv'.format(league_string.lower(), stat.replace(' ', '').lower()), 'w', newline='') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      dict_writer.writerows(lines)

  
