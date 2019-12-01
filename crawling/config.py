import pandas as pd
import numpy as np
import csv
import requests
from bs4 import BeautifulSoup
import os
class Config:
    def __init__(self):

        self.api_key = 'RGAPI-5a786c3d-9ee9-4df5-8bdf-631243a7af38'
        self.summoner_name_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
        self.tier_url = "https://kr.api.riotgames.com/lol/league/v4/positions/by-summoner/"
        self.current_game_url = "https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
        self.match_history = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"
        self.champ_mastery = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"
        self.opgg_user_url = 'https://www.op.gg/summoner/userName='
        self.LaneRecommendByChamp = {}

        reader = csv.reader(open('./crawling/champion_list.csv', 'r'))
        self.champion_list = {}
        for row in reader:
            if len(row) != 3: continue
            k, v, t = row
            self.champion_list[k] = [v, t]

        self.make_RecommendLaneFromChamping_csv()

        reader = csv.reader(open('./crawling/spell_list.csv', 'r'))
        self.spell_list = {}
        for row in reader:
            if len(row) != 3: continue
            k, v, t = row
            self.spell_list[k] = [v, t]


        reader = csv.reader(open('./crawling/item_list.csv', 'r'))
        self.item_list = {}
        for row in reader:
            if len(row) != 2: continue
            k, v = row
            self.item_list[k] = v

    def RecommendLaneFromChampion(self, champion_name):
        champ_stats_url = self.get_champ_stat_url(champion_name)
        search = requests.get(champ_stats_url)
        html = search.text
        champ_soup = BeautifulSoup(html, 'html.parser')

        # Get champion lanes
        html_lane_class = ".champion-stats-header__position.champion-stats-header__position "
        lanes = [e.text for e in champ_soup.select(html_lane_class + "span.champion-stats-header__position__role")]
        lane_rates = [e.text for e in champ_soup.select(html_lane_class + "span.champion-stats-header__position__rate")]
        champion_lanes_list = {}
        for i, j in zip(lanes, lane_rates):
            champion_lanes_list[i] = float(j[:-1])
        if len(champion_lanes_list) == 0 : return 'Top'
        return list(champion_lanes_list.items())[
            (list(champion_lanes_list.values())).index(max(champion_lanes_list.values()))]
    def make_RecommendLaneFromChamping_csv(self):

        if 'recommend.csv' in os.listdir('.'):
            with open('./recommend.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.LaneRecommendByChamp = row
        else:
            with open('./recommend.csv', 'w') as f:
                for index, val in enumerate(self.champion_list.values()):
                    self.LaneRecommendByChamp[val[0]] = self.RecommendLaneFromChampion(val[0])[0]
                writer = csv.DictWriter(f, fieldnames=self.LaneRecommendByChamp.keys())
                writer.writeheader()
                writer.writerow(self.LaneRecommendByChamp)



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

