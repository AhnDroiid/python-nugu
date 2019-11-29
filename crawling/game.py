import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from config import Config

config = Config()
API_KEY = config.api_key

SUMMONER_NAME_URL = config.summoner_name_url
TIER_URL = config.tier_url
MATCH_HISTORY = config.match_history
CHAMP_MASTERY = config.champ_mastery

OPGG_USER_URL = config.opgg_user_url

class Game:

    def __init__(self, player_name, json_game_info):
        self.nugu_player = player_name
        self.participants = json_game_info['participants']
        self.bannedChampions  = json_game_info['bannedChampions']
        self.gameLength = None

        self.players_name = []
        self.players_id = []
        self.players_rune_tree = []
        self.players_level = []
        self.players_champion = []
        self.players_spell = []
        
        for player in self.participants:
            self.players_name.append(player['summonerName'])
            self.players_id.append(player['summonerId'])
            self.players_level.append(requests.get(SUMMONER_NAME_URL + player['summonerName'] +'?api_key=' + API_KEY).json()['summonerLevel'])
            self.players_rune_tree.append(player['perks']['perkIds'])
            self.players_champion.append(config.champion_list[str(player['championId'])])
            self.players_spell.append([ config.spell_list[str(player['spell1Id'])], 
                                           config.spell_list[str(player['spell2Id'])] ])


    def level_of_champion(self, idx):####
        print(CHAMP_MASTERY + str(self.players_id[idx]) + "/by-chamion/"
                                    + str(self.participants[idx]['championId']) + '?api_key=' + API_KEY)
        mastery_info = requests.get(CHAMP_MASTERY + str(self.players_id[idx]) + "/by-champion/"
                                    + str(self.participants[idx]['championId']) + '?api_key=' + API_KEY).json()
        champion_level = mastery_info['championLevel']
        champion_point = mastery_info['championPoints']
        

        return champion_level, champion_point
