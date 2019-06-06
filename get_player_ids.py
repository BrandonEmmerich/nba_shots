import json
import requests
import settings

response = requests.get(
    'https://stats.nba.com/stats/leaguedashplayerstats',
    headers=settings.HEADERS_NBA_DOT_COM,
    params=settings.PARAMETERS_PLAYER_STATS)

data = response.json()['resultSets'][0]['rowSet']

player_id_data = {
    'season': response.json()['parameters']['Season'],
    'player_data': []
}

for element in data:
    row = {
        'player_id': element[0],
        'player_name': element[1],
    }
    player_id_data['player_data'].append(row)

with open('data/player_id_data.json', 'w') as outfile:
        json.dump(player_id_data, outfile)
