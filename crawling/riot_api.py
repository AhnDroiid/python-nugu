import requests
from bs4 import BeautifulSoup
import os
import sys

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .game import Game
from .config import Config
from random import randint
import time
from datetime import datetime
config = Config()
API_KEY = config.api_key

SUMMONER_NAME_URL = config.summoner_name_url
TIER_URL = config.tier_url
CURRENT_GAME_URL = config.current_game_url
MATCH_HISTORY = config.match_history
CHAMP_MASTERY = config.champ_mastery
OPGG_USER_URL = config.opgg_user_url



def PlayMusic(**kwargs):

    return [{
    'type': 'AudioPlayer.Play',
    'audioItem': {
      'stream': {
        'url': 'https://www.youtube.com/watch?v=nRrXhgEqJMI&t=1913s',
        'offsetInMilliseconds': 0,
        'token': 'OK',
        'expectedPreviousToken': 'expectedPreviousToken',
      }
    }
  }]

# def StopMusic(**kwargs):
#





def Eng2Kor(name, arg):
    if arg == 'item':
        return config.item_list[name]
        # for key in config.item_list.keys():
        #     if name in key:
        #         return val[-1]
    if arg == 'champion':
        for value in config.champion_list.values():
            if name in value:
                return value[1]
    if arg == "spell":
        for value in config.spell_list.values():
            if name in value:
                return value[1]

def Kor2Eng(name, arg):
    if arg == 'champion' :
        for value in config.champion_list.values():
            if name in value:
                return value[0]

    elif arg == 'spell':
        for value in config.spell_list.values():
            if name in value:
                return value[0]
    elif arg == "lane":
        if name == "탑":
            return "Top"
        elif name == "원딜":
            return "Bottom"
        elif name == "서폿":
            return "Support"
        elif name == "미드":
            return "Middle"
        else: return "Jungle"

def get_player_id(player_name):  # initialization function
    r = requests.get(SUMMONER_NAME_URL + player_name + '?api_key=' + API_KEY)
    return r.json()['id'], r.json()['accountId']


####################################################################################
def Specific_PlayerSummary(**kwargs):  # answer.opponent.specific
    champ_name = kwargs['NAME_OPPONENT_CHAMPION_FOR_ANALYSIS']
    current_game = kwargs['current_game']
    idx = -1
    for index, champs in enumerate(current_game.players_champion):
        # print(champs)
        if champ_name in champs:
            idx = index
    if idx == - 1: return {'OPPONENT_CHAMPION_TEAR': "error", 'OPPONENT_CHAMPION_WINNING_RATE': "error",
                    'OPPONENT_CAUTION_CHAMPION': "error"}

    player_name = current_game.players_name[idx]
    search = requests.get(OPGG_USER_URL + player_name)
    html = search.text
    user_soup = BeautifulSoup(html, 'html.parser')
    tier_data = user_soup.select('.TierRank')[0].text.strip()
    user_most_champs = []
    if tier_data != 'Unranked':
        raw_data = user_soup.find("meta", {"name": "description"}).get('content')
        user_data = raw_data.split('/')
        user_tier = user_data[1].split(' ')[1:-1]
        # user_winning_rate = user_data[2].split(' ')[-2]

        user_recent_winning_rate = user_soup.find_all('div', attrs={'class': 'Text'})
        # print(user_recent_winning_rate)
        user_recent_winning_rate = [elem.text for elem in user_recent_winning_rate if '%' in elem.text]
        #user_recent_winning_rate = user_soup.select('.WinRatioGraph div.Text')[0].text
        user_most_champs_raw = user_data[3].split(',')[:3]

        for champ in user_most_champs_raw:
            tmp = champ.replace(' ', '', 1)
            user_most_champs.append(tmp.replace(' -', '', 1).split(' '))
        return {'OPPONENT_CHAMPION_TEAR': user_tier[0], 'OPPONENT_CHAMPION_WINNING_RATE': user_recent_winning_rate[0]}
    else:
        user_most_champs_raw = user_soup.select('.ChampionBox.Ranked div.ChampionInfo a')
        user_most_champs_winning_rate = user_soup.select('.ChampionBox.Ranked div.Played')
        for champ, winning_rate in zip(user_most_champs_raw, user_most_champs_winning_rate):
            user_most_champs.append(champ.text.strip())
        user_recent_winning_rate = user_soup.find_all('div', attrs={'class': 'Text'})
        # print(user_recent_winning_rate)
        user_recent_winning_rate = [elem.text for elem in user_recent_winning_rate if '%' in elem.text]
        #user_recent_winning_rate = user_soup.select('.WinRatioGraph div.Text')[0].text
        return {'OPPONENT_CHAMPION_TEAR': tier_data, 'OPPONENT_CHAMPION_WINNING_RATE': user_recent_winning_rate[0]}

    # search = requests.get(OPGG_USER_URL + player_name)
    #
    # html = search.text
    # user_soup = BeautifulSoup(html, 'html.parser')
    #
    # raw_data = user_soup.find("meta", {"name": "description"}).get('content')
    # user_data = raw_data.split('/')
    #
    # user_tier = user_data[1].split(' ')[1:-1]
    # user_winning_rate = user_data[2].split(' ')[-2]
    # user_most_champs_raw = user_data[3].split(',')[:3]
    # user_most_champs = []
    # for champ in user_most_champs_raw:
    #     tmp = champ.replace(' ', '', 1)
    #     user_most_champs.append(tmp.replace(' -', '', 1).split(' '))
    #
    # return {'OPPONENT_CHAMPION_TEAR': user_tier[0], 'OPPONENT_CHAMPION_WINNING_RATE': user_winning_rate,
    #         'OPPONENT_CAUTION_CHAMPION': user_most_champs[0][0]}

def player_summary(player_name):
    search = requests.get(OPGG_USER_URL + player_name)
    html = search.text
    user_soup = BeautifulSoup(html, 'html.parser')
    tier_data = user_soup.select('.TierRank')[0].text.strip()
    user_most_champs = []
    if tier_data != 'Unranked':
        raw_data = user_soup.find("meta", {"name": "description"}).get('content')
        user_data = raw_data.split('/')
        user_tier = user_data[1].split(' ')[1:-1]
        # user_winning_rate = user_data[2].split(' ')[-2]
        user_recent_winning_rate = user_soup.select('.WinRatioGraph div.Text')[0].text
        user_most_champs_raw = user_data[3].split(',')[:3]
        for champ in user_most_champs_raw:
            tmp = champ.replace(' ', '', 1)
            user_most_champs.append(tmp.replace(' -', '', 1).split(' '))
        return {'OPPONENT_CHAMPION_TEAR': user_tier[0], 'OPPONENT_CHAMPION_WINNING_RATE': user_recent_winning_rate,
                'OPPONENT_CAUTION_CHAMPION': user_most_champs[0][0]}
    else:
        user_most_champs_raw = user_soup.select('.ChampionBox.Ranked div.ChampionInfo a')
        user_most_champs_winning_rate = user_soup.select('.ChampionBox.Ranked div.Played')
        for champ, winning_rate in zip(user_most_champs_raw, user_most_champs_winning_rate):
            user_most_champs.append(champ.text.strip())
        user_recent_winning_rate = user_soup.select('.WinRatioGraph div.Text')[0].text
        return {'OPPONENT_CHAMPION_TEAR': tier_data, 'OPPONENT_CHAMPION_WINNING_RATE': user_recent_winning_rate, 'OPPONENT_CAUTION_CHAMPION': user_most_champs[0]}



def Total_PlayerSummary(**kwargs):  #  answer.opponent.caution_champion
    currGame = kwargs['current_game']
    temp_lst = [player_summary['OPPONENT_CHAMPION_WINNING_RATE'] for player_summary in currGame.players_summary]
    return_idx = temp_lst.index(max(temp_lst))
    # print(currGame.players_champion)
    return {'OPPONENT_CHAMPION_TEAR': currGame.players_summary[return_idx]['OPPONENT_CHAMPION_TEAR'],
            'OPPONENT_CHAMPION_WINNING_RATE': currGame.players_summary[return_idx]['OPPONENT_CHAMPION_WINNING_RATE'],
            'OPPONENT_CAUTION_CHAMPION': currGame.players_champion[return_idx][1]}
    # result = {'OPPONENT_CHAMPION_TEAR': [], 'OPPONENT_CHAMPION_WINNING_RATE': []}
    # for player in player_name_list:
    #     spec = player_summary(player)
    #     result['OPPONENT_CHAMPION_TEAR'].append(spec['OPPONENT_CHAMPION_TEAR'])
    #     result['OPPONENT_CHAMPION_WINNING_RATE'].append(spec['OPPONENT_CHAMPION_WINNING_RATE'])
        #result['OPPONENT_CAUTION_CHAMPION'].append(spec['OPPONENT_CAUTION_CHAMPION'])
    
    #  champ_name = result['OPPONENT_CAUTION_CHAMPION'][return_idx]
    # #print(result)
    # #print(config.champion_list.values())
    # for champs in config.champion_list.values():
    #     if champ_name in champs[0]:
    #         champ_name = champs[1]

def RecommendChampionFromChampion(**kwargs):
    champion_name = Kor2Eng(kwargs['NAME_OPPONENT_CHAMPION'], 'champion')
    # print(champion_name)
    # Get info. of counters
    champ_stats_url = config.get_champ_stat_url(champion_name)
    search = requests.get(champ_stats_url)
    html = search.text
    champ_soup = BeautifulSoup(html, 'html.parser')

    get_counter_url = ".champion-stats-header-matchup__table.champion-stats-header-matchup__table--strong.tabItem "
    # counters = champ_soup.find_all('tr', attrs={'data-champion-id'})
    counters = champ_soup.select(get_counter_url + "img")
    most_counter = str(counters[0]).split('.png?')[0].split('/')[-1]
    # print(abc)
    # counters_winning_rate = champ_soup.select(get_counter_url + "b")
    # counter_list = []
    # for i, j in zip(counters[0::2], counters_winning_rate):
    #     counter_list.append([i.text.strip(), j.text])
    # print(counter_list)
    # print(Eng2Kor(counter_list[0][0], 'champion'))
    return {'RECOMMENDED_CHAMPION': Eng2Kor(most_counter, 'champion')}

def CheckFriendStatus(**kwarg):
    if kwarg['NAME_FRIEND'] in config.friend.keys():
        search = requests.get(OPGG_USER_URL + config.friend[kwarg['NAME_FRIEND']])
        html = search.text
        user_soup = BeautifulSoup(html, 'html.parser')
        live = user_soup.select(".SpectatorError")
        if len(live) == 0:  return {'STATUS_LOG_IN': 2}
        else: return {'STATUS_LOG_IN': 1}
    else:
        return {'STATUS_LOG_IN': 3}


def RecommendChampionFromLane(**kwargs):
    lane_name = Kor2Eng(kwargs['NAME_LANE'], 'lane')
    lane_index = list(config.LaneRecommendByChamp.values()).index(lane_name)
    return {'RECOMMENDED_CHAMPION': Eng2Kor(list(config.LaneRecommendByChamp.keys())[lane_index], 'champion')}

def RecommendRandomChampion(**kwargs):
    return {'RECOMMENDED_CHAMPION': list(((config.champion_list).values()))[randint(0, len(list(config.champion_list)))][1]}


def RecommendSkillSpecific(**kwargs):

    champion_name = Kor2Eng(kwargs['NAME_CHAMPION'], 'champion')
    champion_level = int(kwargs['NAME_LEVEL'][:-2])

    champ_stats_url = config.get_champ_stat_url(champion_name)
    search = requests.get(champ_stats_url)
    html = search.text
    champ_soup = BeautifulSoup(html, 'html.parser')

    # Get a skill tree
    skill_tree = champ_soup.select(".champion-skill-build__table td")
    skill_tree_recommend = []
    for skill in skill_tree:
        skill_tree_recommend.append(skill.text.strip())
    while len(skill_tree_recommend) != 18:
        skill_tree_recommend.append(skill_tree_recommend[-1])
    # print(skill_tree_recommend[champion_level])
    return {'RECOMMENDED_SKILL_SPECIFIC': skill_tree_recommend[champion_level]}

def RecommendSkillAll(**kwargs):

    champion_name = Kor2Eng(kwargs['NAME_CHAMPION'], 'champion')
    #champion_level = int(kwargs['NAME_LEVEL'])

    champ_stats_url = config.get_champ_stat_url(champion_name)
    search = requests.get(champ_stats_url)
    html = search.text
    champ_soup = BeautifulSoup(html, 'html.parser')

    # Get a skill-mastery [w, q, e]
    skill_mastery = champ_soup.select(".champion-stats__list__item span")
    skill_mastery_recommend = []
    for skill in skill_mastery:
        skill_mastery_recommend.append(skill.text)
    # print(skill_mastery_recommend[0])
    # print(skill_mastery_recommend[1])
    # print(skill_mastery_recommend[2])

    return {'RECOMMENDED_SKILL_1ST': skill_mastery_recommend[0], 'RECOMMENDED_SKILL_2ST': skill_mastery_recommend[1], 'RECOMMENDED_SKILL_3ST': skill_mastery_recommend[2]}



def RecommendItemSpecific(**kwargs):

    champion_name = Kor2Eng(kwargs['NAME_CHAMPION_FOR_ITEM'] , 'champion')
    core_num = int(kwargs['NAME_NUMBER_ITEM_CORE'][:-2])

    champ_stats_url = config.get_champ_stat_url(champion_name)
    search = requests.get(champ_stats_url)
    html = search.text
    champ_soup = BeautifulSoup(html, 'html.parser')

    item_recommend_list = []
    items = champ_soup.select(".champion-overview__row.champion-overview__row")
    for item in items:
        item_names = item.select(".champion-stats__list__item")
        tmp = []
        for item_name in item_names:
            tmp.append(str(item_name).split('&gt')[1].split(';')[1][:-3])
        tmp.append(item.select(".champion-overview__stats.champion-overview__stats--win.champion-overview__border")[
                       0].text.split('\n')[1])  # get item winning rate

        item_recommend_list.append(tmp)


    return {'RECOMMENDED_ITEM_SPECIFIC': Eng2Kor(item_recommend_list[2][core_num - 1], 'item')}

def RecordSpellTime(**kwargs):   # write_used_spell action,  RECORD TIME WHEN SPELL IS USED
    current_game = kwargs['current_game']
    champion_name = Kor2Eng(kwargs['NAME_CHAMPION_FOR_SPELL_RECORD'], 'champion')
    spell_name = Kor2Eng(kwargs['NAME_USED_SPELL'], 'spell')
    now_time = datetime.now()
    now_time_in_second = now_time.hour * 3600 + now_time.minute * 60 + now_time.second
    current_game.players_spell_used_time[champion_name][spell_name] = now_time_in_second


def AnswerSpellRemainingTime(**kwargs):    # answer specific champion spell time
    current_game = kwargs['current_game']
    champion_name = Kor2Eng(kwargs['NAME_CHAMPION_FOR_SPELL'] , 'champion')
    asked_spell_name = Kor2Eng(kwargs['NAME_SPELL'], 'spell')



    now_time = datetime.now()
    now_time_in_second = now_time.hour * 3600 + now_time.minute * 60 + now_time.second

    champion_index = list(current_game.players_spell_used_time.keys()).index(champion_name)

    for spell in config.spell_list.values():
        if spell[0] == asked_spell_name:
            cool_time = spell[2]



    remain_time = int(cool_time) - int((now_time_in_second - current_game.players_spell_used_time[champion_name][asked_spell_name]))


    current_game.players_spell_used_time[champion_name][asked_spell_name] = now_time_in_second

    # print(current_game.players_spell_used_time)
    # print(remain_time)

    if remain_time > 0 :
        return {'REMAINING_TIME_OF_SPELL': str(remain_time)}

    else: return {'REMAINING_TIME_OF_SPELL': 0}


def AnswerSpellRemainingTimeAll(**kwargs):    # answer specific champion spell time
    current_game = kwargs['current_game']
    champion_name = Kor2Eng(kwargs['NAME_CHAMPION_FOR_SPELL'] , 'champion')


    now_time = datetime.now()
    now_time_in_second = now_time.hour * 3600 + now_time.minute * 60 + now_time.second

    #champion_index = list(current_game.players_spell_used_time.keys()).index(champion_name)



    for index, spell in enumerate(list(current_game.players_spell_used_time[champion_name].keys())):
        for spell_name in config.spell_list.values():
            if spell == spell_name[0]:
                cool_time = spell_name[2]
        if index == 0:
            remain_time_1 = int(cool_time) - int((now_time_in_second - current_game.players_spell_used_time[champion_name][spell]))
        elif index == 1:
            remain_time_2 = int(cool_time) - int((now_time_in_second - current_game.players_spell_used_time[champion_name][spell]))



    #current_game.players_spell_used_time[champion_name][asked_spell_name] = now_time_in_second



    return {'SPELL_NAME1' : Eng2Kor(list(current_game.players_spell_used_time[champion_name].keys())[0], 'spell') , 'REMAINING_TIME1': max(0, remain_time_1),
                'SPELL_NAME2': Eng2Kor(list(current_game.players_spell_used_time[champion_name].keys())[1], 'spell') , 'REMAINING_TIME2': max(0, remain_time_2)}





def RecommendItemAll(**kwargs):

    champion_name = Kor2Eng(kwargs['NAME_CHAMPION_FOR_ITEM'] , 'champion')
    champ_stats_url = config.get_champ_stat_url(champion_name)
    search = requests.get(champ_stats_url)
    html = search.text
    champ_soup = BeautifulSoup(html, 'html.parser')

    item_recommend_list = []
    items = champ_soup.select(".champion-overview__row.champion-overview__row")
    for item in items:
        item_names = item.select(".champion-stats__list__item")
        tmp = []
        for item_name in item_names:
            tmp.append(str(item_name).split('&gt')[1].split(';')[1][:-3])
        tmp.append(item.select(".champion-overview__stats.champion-overview__stats--win.champion-overview__border")[
                       0].text.split('\n')[1])  # get item winning rate
        item_recommend_list.append(tmp)
    # print(item_recommend_list)
    return {'RECOMMENDED_ITEM_1ST': Eng2Kor(item_recommend_list[2][0], 'item'), 'RECOMMENDED_ITEM_2ST': Eng2Kor(item_recommend_list[2][1], 'item'),'RECOMMENDED_ITEM_3ST':  Eng2Kor(item_recommend_list[2][2], 'item')}


def ChamionSummary(champion_name, lane=''):
    champ_stats_url = config.get_champ_stat_url(champion_name)
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
    # print(champion_lanes_list)

    # Get recommended spells
    spells = champ_soup.select(".champion-stats__list__item img.tip")
    spells_winning_rate = champ_soup.select(".champion-overview__stats.champion-overview__stats--win strong")
    spell_recommend = []
    idx = 0
    tmp = []
    for spell in spells:
        tmp.append(str(spell).split('&gt;')[1].split('&lt')[0])
        idx += 1
        if idx % 2 == 0:
            tmp.append(spells_winning_rate[int(idx / 2) - 1].text)
            spell_recommend.append(tmp)
            tmp = []
    # print(spell_recommend)

    # Get a skill-mastery [w, q, e]
    skill_mastery = champ_soup.select(".champion-stats__list__item span")
    skill_mastery_recommend = []
    for skill in skill_mastery:
        skill_mastery_recommend.append(skill.text)
    # print(skill_mastery_recommend)
    # Get a skill tree
    skill_tree = champ_soup.select(".champion-skill-build__table td")
    skill_tree_recommend = []
    for skill in skill_tree:
        skill_tree_recommend.append(skill.text.strip())
    while len(skill_tree_recommend) != 18:
        skill_tree_recommend.append(skill_tree_recommend[-1])
    # print(skill_tree_recommend)
    # Get a rune and winning rate
    runes = champ_soup.select(".champion-stats-summary-rune__name")
    rune_rates = champ_soup.select(".champion-stats-summary-rune__rate span")
    rune_rates = [e.text for e in rune_rates if e.text not in ('Pick Rate', 'Win Rate')]

    recommend_rune_list = []
    for rune, rune_rate in zip(runes, rune_rates):
        recommend_rune_list.append([rune.text, rune_rate])
    # print(recommend_rune_list)
    # Get a detailed tree
    rune_detail = champ_soup.select(".perk-page__item.perk-page__item--active img")
    rune_detail_winning_rate = champ_soup.select(".champion-overview__stats.champion-overview__stats--pick strong")
    rune_detail_winning_rate = rune_detail_winning_rate[-8:][1::2]
    rune_detailed_list = []
    idx = 0
    tmp = []
    for rune in rune_detail:
        tmp.append(str(rune).split('"')[1])
        idx += 1
        if idx % 6 == 0:
            tmp.append(rune_detail_winning_rate[int(idx / 6) - 1].text)
            rune_detailed_list.append(tmp)
            tmp = []

    #RecommendSkillSpecific Get a item tree and winning rate
    item_recommend_list = []
    items = champ_soup.select(".champion-overview__row.champion-overview__row")
    for item in items:
        item_names = item.select(".champion-stats__list__item")
        tmp = []
        for item_name in item_names:
            tmp.append(str(item_name).split('&gt')[1].split(';')[1][:-3])
        tmp.append(item.select(".champion-overview__stats.champion-overview__stats--win.champion-overview__border")[
                       0].text.split('\n')[1])  # get item winning rate
        item_recommend_list.append(tmp)
    # print(item_recommend_list)



# champion_name = kwargs['NAME_CHAMPION']
# champion_level = int(kwargs['NAME_LEVEL'][:-2])

#print(RecommendChampionFromLane('Top'))
#print(RecommendChampionFromChampion('Ashe'))

#print(RecommendChampionFromChampion(**args))# print(RecommendSkillAll(**args))
# # #

#
# player_name = "real gankster"
#
#
#
# chamion_name = 'Ashe'
# champ_summary = ChamionSummary(chamion_name)
# player_id, account_id = get_player_id(player_name)
#
#
#
# # current game!
#
# response = requests.get(CURRENT_GAME_URL + player_id +'?api_key=' + API_KEY)
# if response.status_code == 404:
#     print('{}님은 현재 게임 중이 아닙니다.'.format(player_name))
#     exit(-1)
#
# current_game_info = response.json()
#
# current_game = Game(player_name, current_game_info)
#
# print(current_game.players_rune_tree)
#

#
#
#
#
# args = {'NAME_OPPONENT_CHAMPION': '갱플랭크'}
# RecommendChampionFromChampion(**args)


# args = {'current_game' : current_game}
# Total_PlayerSummary(**args)

# args = {'NAME_LANE': '탑'}
# print(RecommendChampionFromLane(**args))