import json
import requests
import settings


def get_shot_data(player_id):
    params = (('PlayerID', str(player_id)),) + settings.PARAMETERS_SHOT_DATA

    response = requests.get(
        'https://stats.nba.com/stats/shotchartdetail',
        headers=settings.HEADERS_NBA_DOT_COM,
        params=params)

    return response.json()['resultSets'][0]


def get_player_ids():
    with open('data/player_id_data.json') as json_file:
        player_id_data = json.load(json_file)

    return [player['player_id'] for player in player_id_data['player_data']]


def parse_player_shots(data):
    data_keys = data['headers']
    full_data = data['rowSet']

    player_shots = []
    for element in full_data:
        row = dict(zip(data_keys, element))
        player_shots.append(row)

    return player_shots

if __name__ == '__main__':
    player_ids = get_player_ids()

    all_shot_data = {
        'data': [],
    }

    for k, player_id in enumerate(player_ids):
        try:
            print('Player ID: ' + str(player_id))
            percent_complete = 100 * k / len(player_ids)
            print('Percent Complete: ' + str(percent_complete))

            shot_data = get_shot_data(player_id)
            parsed_data = parse_player_shots(shot_data)

            print('Player Name: ' + parsed_data[0]['PLAYER_NAME'])

            row = {
                'player_id': player_id,
                'shots': parsed_data,
            }

            all_shot_data['data'].append(row)

        except Exception as e:
            print(e)


    number_of_players = len(all_shot_data['data'])
    chunk_size = 150

    for i in xrange(0, number_of_players, chunk_size):
        with open('data/shot_data_file_' + str(i//chunk_size + 1) + '.json', 'w') as outfile:
            chunk_of_data = {
                'data': all_shot_data['data'][i:i + chunk_size]
                }
            json.dump(chunk_of_data, outfile)
