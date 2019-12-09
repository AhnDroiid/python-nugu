from flask import Flask, render_template, request
import json
from query_processor import game_needed_answer, game_not_needed_answer, query_config
from crawling import game, config
from crawling.riot_api import *
from urllib import parse
app = Flask(__name__)

player_name = "real gankster"
player_name_url = parse.quote(player_name)
player_id, account_id = get_player_id(player_name_url)
config_dat = Config()

current_game = None

@app.route('/', methods=['POST'])
def post():
	global current_game
	query = request.json

	print(query)

	actionName = query['action']['actionName']

	for query_dat in query_config:
		print(query_dat)
		if query_dat['action_name'] == actionName and query_dat['need'] == True:
			print("CURRENT GAME DATA IS NEEDED")
			## current game!
			response = requests.get(CURRENT_GAME_URL + player_id + '?api_key=' + API_KEY)
			if response.status_code == 404:
				print('{}님은 현재 게임 중이 아닙니다.'.format(player_name))

			if current_game is None:
				print("CURRENT GAME IS EMPTY")
				print("GAME IS INITIALIZED")
				print("PLEASE WAIT...")
				current_game_info = response.json()
				current_game = Game(player_name, current_game_info)
			return json.dumps(game_needed_answer(query, current_game), ensure_ascii=False, indent=4)

		elif query_dat['action_name'] == actionName and query_dat['need'] == False:
			print("CURRENT GAME DATA IS NOT NEEDED")
			return json.dumps(game_not_needed_answer(query), ensure_ascii=False, indent=4)

		else:
			return json.dumps(game_not_needed_answer(query), ensure_ascii=False, indent=4)

app.run(host='0.0.0.0', port=3389)


