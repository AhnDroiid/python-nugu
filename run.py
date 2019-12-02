from flask import Flask, render_template, request
import json
from query_processor import answer
from crawling import game, config
from crawling.riot_api import *
from urllib import parse
app = Flask(__name__)

player_name = "jgggggg"
player_name_url = parse.quote(player_name)
player_id, account_id = get_player_id(player_name_url)
#chamion_name = 'ekko'
#champ_summary = ChamionSummary(chamion_name)
config_dat = Config()

## current game!
response = requests.get(CURRENT_GAME_URL + player_id + '?api_key=' + API_KEY)
if response.status_code == 404:
	print('{}님은 현재 게임 중이 아닙니다.'.format(player_name))
	#exit(-1)

current_game_info = response.json()
current_game = Game(player_name, current_game_info)


@app.route('/', methods=['POST'])
def post():
	global current_game

	print(current_game.players_spell_used_time)
	query = request.json
	#response = requests.get(CURRENT_GAME_URL + player_id + '?api_key=' + API_KEY)
	#current_game_info_query = response.json()
	# if current_game.checkId(current_game_info_query['gameId']):
	# 	pass
	# else:
	# 	current_game = Game(player_name, current_game_info_query)
	print(query)

	return json.dumps(answer(query, current_game), ensure_ascii=False, indent=4)
	#flag, response, current_game_new = answer(query, current_game)

	# if flag == 1:
	# 	return json.dumps(response, ensure_ascii=False, indent=4)
	# else:
	# 	current_game = current_game_new
	# 	return json.dumps(response, ensure_ascii=False, indent=4)

app.run(host='0.0.0.0', port=3389)

# query = {'action': {'actionName': 'write.used_spell', 'parameters' : {'NAME_CHAMPION_FOR_SPELL_RECORD' : {'value': 'Ashe'}, 'NAME_USED_SPELL': {'value': 'Ignite'}}}}
# flag, response, current_game_new = answer(query, current_game)
# print(query)
# print(response)


