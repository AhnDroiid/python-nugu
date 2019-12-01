from flask import Flask, render_template, request
import json
from query_processor import answer
from crawling import game, config
from crawling.riot_api import *

app = Flask(__name__)

player_name = "SKT T1 Roach"
player_id, account_id = get_player_id(player_name)
chamion_name = 'ekko'
champ_summary = ChamionSummary(chamion_name)
config_dat = Config()


## current game!
response = requests.get(CURRENT_GAME_URL + player_id + '?api_key=' + API_KEY)
if response.status_code == 404:
	print('{}님은 현재 게임 중이 아닙니다.'.format(player_name))
	exit(-1)

current_game_info = response.json()
current_game = Game(player_name, current_game_info)

@app.route('/', methods=['POST'])
def post():
	global current_game
	query = request.json

	print(query)
	flag, response, current_game_new = answer(query, current_game)

	if flag == 1:
		return json.dumps(response, ensure_ascii=False, indent=4)
	else:
		current_game = current_game_new
		return json.dumps(response, ensure_ascii=False, indent=4)

app.run(host='0.0.0.0', port=3389)


