from flask import Flask, render_template, request
import json
from query_processor import answer
from crawling import game, config
from crawling.riot_api import *

app = Flask(__name__)

player_name = "Hanabi1"
player_id, account_id = get_player_id(player_name)
chamion_name = 'ekko'
champ_summary = ChamionSummary(chamion_name)


## current game!
response = requests.get(CURRENT_GAME_URL + player_id + '?api_key=' + API_KEY)
if response.status_code == 404:
	print('{}님은 현재 게임 중이 아닙니다.'.format(player_name))
	exit(-1)

current_game_info = response.json()
current_game = Game(player_name, current_game_info)


@app.route('/', methods=['POST'])
def post():
	query = request.json

	print(query)
	return json.dumps(answer(query, current_game), ensure_ascii=False, indent=4)


app.run(host='0.0.0.0', port=3389)


