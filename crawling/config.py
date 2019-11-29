import pandas as pd
import numpy as np
import csv

class Config:
    def __init__(self):

        self.api_key = 'RGAPI-880ae7e9-0de1-47f2-a1df-da1a0a9820d1'
        self.summoner_name_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
        self.tier_url = "https://kr.api.riotgames.com/lol/league/v4/positions/by-summoner/"
        self.current_game_url = "https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
        self.match_history = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"
        self.champ_mastery = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"
        self.opgg_user_url = 'https://www.op.gg/summoner/userName='
        
        reader = csv.reader(open('champion_list.csv', 'r'))
        self.champion_list = {}
        for row in reader:
            k, v = row
            self.champion_list[k] = v
        
        reader = csv.reader(open('spell_list.csv', 'r'))
        self.spell_list = {}
        for row in reader:
            k, v = row
            self.spell_list[k] = v

        reader = csv.reader(open('item_list.csv', 'r'))
        self.item_list = {}
        for row in reader:
            k, v = row
            self.item_list[k] = v

        
    def get_champ_stat_url(self, name):
        return 'https://www.op.gg/champion/{}/statistics/mid'.format(name)

######################################## ignore these lines
# champion_id_url = requests.get("http://ddragon.leagueoflegends.com/cdn/9.23.1/data/en_US/item.json")
# champion_id_json = champion_id_url.json()

# champion_id_dict = champion_id_json['data']


# with open('item_list.csv', 'a') as f:
#     logging = csv.writer(f, delimiter=",")
#     for k, v in champion_id_dict.items():
#         logging.writerow([v['name'], v['plaintext']])
#         # for k, v in champion_id_dict.items():
# #     print(v['name'])
#     f.close()

