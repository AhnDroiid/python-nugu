import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from . import config

config = config.Config()
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
        self.players_spell_used_time = {}
        self.currId = json_game_info['gameId']
        self.teamId = None
        for player in self.participants:
            # print(type(player['summonerName']))
            # print(type(self.nugu_player.strip()))
            if player['summonerName'] == self.nugu_player.strip():
                print(player)
                print(player['teamId'])
                self.teamId = player['teamId']

        for player in self.participants:
            if player['teamId'] != self.teamId:
                self.players_name.append(player['summonerName'])
                self.players_id.append(player['summonerId'])
                self.players_level.append(requests.get(SUMMONER_NAME_URL + player['summonerName'] +'?api_key=' + API_KEY).json()['summonerLevel'])
                self.players_rune_tree.append(player['perks']['perkIds'])
                self.players_champion.append(config.champion_list[str(player['championId'])])
                self.players_spell.append([config.spell_list[str(player['spell1Id'])],
                                               config.spell_list[str(player['spell2Id'])] ])
        for index, item in enumerate(self.players_spell):
            spell_1 = item[0]
            spell_2 = item[1]
            self.players_spell_used_time[self.players_champion[index][0]] = {spell_1[1]: -1, spell_2[1]: -1}

#### player_summary: this code is crawled from OP.GG
        self.players_summary = []
        print(self.players_name)
        for player in self.players_name:
            search = requests.get(OPGG_USER_URL + player)
            html = search.text
            user_soup = BeautifulSoup(html, 'html.parser')
            tier_data = user_soup.select('.TierRank')[0].text.strip()
            
            # user_recent_winning_rate = user_soup.select('.WinRatioGraph div.WinRatioGraph-summary div.Text')
            user_recent_winning_rate = user_soup.find_all('div', attrs={'class': 'Text'})
            # print(user_recent_winning_rate)
            user_recent_winning_rate = [elem.text for elem in user_recent_winning_rate if '%' in elem.text]
            print(user_recent_winning_rate)
            self.players_summary.append({'OPPONENT_CHAMPION_TEAR': tier_data, 'OPPONENT_CHAMPION_WINNING_RATE': user_recent_winning_rate})
        
    def checkId(self, id):
        return self.currId == id

    def level_of_champion(self, idx):####
        print(CHAMP_MASTERY + str(self.players_id[idx]) + "/by-chamion/"
                                    + str(self.participants[idx]['championId']) + '?api_key=' + API_KEY)
        mastery_info = requests.get(CHAMP_MASTERY + str(self.players_id[idx]) + "/by-champion/"
                                    + str(self.participants[idx]['championId']) + '?api_key=' + API_KEY).json()
        champion_level = mastery_info['championLevel']
        champion_point = mastery_info['championPoints']


        return champion_level, champion_point

