import requests
from bs4 import BeautifulSoup
from . import game
from . import config

config = config.Config()
API_KEY = config.api_key

SUMMONER_NAME_URL = config.summoner_name_url
TIER_URL = config.tier_url
CURRENT_GAME_URL = config.current_game_url
MATCH_HISTORY = config.match_history
CHAMP_MASTERY = config.champ_mastery
OPGG_USER_URL = config.opgg_user_url


def get_player_id(player_name):  # initialization function
    r = requests.get(SUMMONER_NAME_URL + player_name +'?api_key=' + API_KEY)
    return r.json()['id'], r.json()['accountId']
####################################################################################


def PlayerSummary(player_name):  # answer.opponent.specific , answer.opponent.caution_champion
    search = requests.get(OPGG_USER_URL + player_name)
    html = search.text
    user_soup = BeautifulSoup(html, 'html.parser')

    raw_data = user_soup.find("meta", {"name":"description"}).get('content')
    user_data = raw_data.split('/')

    user_tier = user_data[1].split(' ')[1:-1]
    user_winning_rate = user_data[2].split(' ')[-2]
    user_most_champs_raw = user_data[3].split(',')[:3]
    user_most_champs = []
    for champ in user_most_champs_raw:
        tmp = champ.replace(' ', '',1)
        user_most_champs.append(tmp.replace(' -', '', 1).split(' '))

    return {'OPPONENT_CHAMPION_TEAR': user_tier[0], 'OPPONENT_CHAMPION_WINNING_RATE': user_winning_rate, 'OPPONENT_CAUTION_CHAMPION': user_most_champs[0][0]}

def ChamionSummary(champion_name):

    champ_stats_url = config.get_champ_stat_url(champion_name)
    search = requests.get(champ_stats_url)
    html = search.text
    champ_soup = BeautifulSoup(html, 'html.parser')


    # Get recommended spells
    spells = champ_soup.select(".champion-stats__list__item img.tip")
    spell_recommend = []
    idx = 0
    tmp = []
    for spell in spells:
        tmp.append(str(spell).split('&gt;')[1].split('&lt')[0])
        idx += 1
        if idx % 2 == 0:
            spell_recommend.append(tmp)
            tmp = []
    print(spell_recommend)


    # Get a skill-mastery [w, q, e]
    skill_mastery = champ_soup.select(".champion-stats__list__item span")
    skill_mastery_recommend = []
    for skill in skill_mastery:
        skill_mastery_recommend.append(skill.text)


    # Get a skill tree
    skill_tree = champ_soup.select(".champion-skill-build__table td")
    skill_tree_recommend = []
    for skill in skill_tree:
        skill_tree_recommend.append(skill.text.strip())
    while len(skill_tree_recommend) != 18:
        skill_tree_recommend.append(skill_tree_recommend[-1])


    # Get a rune and winning rate
    runes = champ_soup.select(".champion-stats-summary-rune__name")
    rune_rates = champ_soup.select(".champion-stats-summary-rune__rate span")
    rune_rates = [e.text for e in rune_rates if e.text not in ('Pick Rate', 'Win Rate')]

    recommend_rune_list = []
    for rune, rune_rate in zip(runes, rune_rates):
        recommend_rune_list.append([rune.text, rune_rate])


    # Get a detailed tree
    rune_detail = champ_soup.select(".perk-page__item.perk-page__item--active img")
    rune_detailed_list = []
    idx = 0
    tmp = []
    for rune in rune_detail:
        tmp.append(str(rune).split('"')[1])
        idx += 1
        if idx % 6 == 0:
            rune_detailed_list.append(tmp)
            tmp = []


    # Get a item tree and winning rate
    items = champ_soup.select(".champion-overview__row.champion-overview__row")
    item_recommend_list = []
    for item in items:
        item_names = item.select(".champion-stats__list__item")
        tmp = []
        for item_name in item_names:
            tmp.append( str(item_name).split('&gt')[1].split(';')[1][:-3] )
        tmp.append(item.select(".champion-overview__stats.champion-overview__stats--win.champion-overview__border")[0].text.split('\n')[1])# get item winning rate
        item_recommend_list.append(tmp)

    # Get info. of counters
    get_counter_url = ".champion-stats-header-matchup__table.champion-stats-header-matchup__table--strong.tabItem "
    counters = champ_soup.select(get_counter_url+"img")
    counters_winning_rate = champ_soup.select(get_counter_url+"b")
    counter_list = []
    for i, j in zip(counters[0::2], counters_winning_rate):
        counter_list.append([i.text.strip(), j.text])



if __name__ == "__main__":

    player_name = 'Hidden in Bush'
    ############ --------- PLAYER SUMMARY ---------- ############
    # player_summary = PlayerSummary(player_name)
    # print(player_summary)



    # chamion_name = 'aurelionsol'
    # champ_summary = ChamionSummary(chamion_name)
    # # print(champ_data.find_all("span"))# print(champ_data.get("span")


    player_id, account_id = get_player_id(player_name)

    # print(player_id)
    # print(account_id)
    # r = requests.get(MATCH_HISTORY + account_id + '?api_key=' + API_KEY).json()
    # print(r)

    ## current game!
    print(PlayerSummary(player_name))
    try:
        current_game_info = requests.get(CURRENT_GAME_URL + player_id +'?api_key=' + API_KEY).json()
        current_game = game.Game(player_name, current_game_info)
    except Exception:
        print('{}is not in game.'.format(player_name))
        exit(-1)


    # print(current_game.participants)
    print(current_game.players_name)
    print(current_game.players_level)
    print(current_game.players_champion)
    print(current_game.players_spell)

    # print(current_game.level_of_champion(0))