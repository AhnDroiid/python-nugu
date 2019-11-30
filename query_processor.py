from crawling.riot_api import *
import sys

player_name = 'Hidden in bush'
player_id, account_id = get_player_id(player_name)



query_config =[
	{'action_name': 'answer.opponent', 'utterance' : ['NAME_OPPONENT_CHAMPION_FOR_ANALYSIS'] , 'backend': ['OPPONENT_CAUTION_CHAMPION', 'OPPONENT_CHAMPION_WINNING_RATE', 'OPPONENT_CHAMPION_TEAR'],
     'function' : PlayerSummary, 'args': player_name, 'action_trigger': 'answer.opponent.specific'
     },
	{'action_name': 'answer.opponent', 'utterance': [], 'backend': ['OPPONENT_CAUTION_CHAMPION', 'OPPONENT_CHAMPION_WINNING_RATE', 'OPPONENT_CHAMPION_TEAR'],
     'function' : PlayerSummary, 'args': player_name,  'action_trigger': 'answer.opponent.caution_champion'
     }

	# {'action_name': 'answer.spell.specific_champion.specific_spell', 'utterance': ['NAME_CHAMPION_FOR_SPELL', 'NAME_SPELL'] , 'backend': ['REMAINING_TIME_OF_SPELL'],
    #  'function' :
    #  },
    #
	# {'action_name': 'answer.spell.specific_champion.wo_specific_spell', 'utterance': ['NAME_CHAMPION_FOR_SPELL', 'NAME_SPELL'], 'backend':['USED_SPELL_NAMES', 'REMAINING_TIMES'],
    #  'function' :
    #  },
    #
	# {'action_name': 'answer.spell.all', 'utterance': ['NAME_CHAMPION_FOR_SPELL', 'NAME_SPELL'], 'backend': ['OPPONENT_CHAMPION1', 'SEPLLS_CHAMPION1', 'REMAINING_TIME_CHAMPION1'],
    #  'function' :
    #  },
    #
	# {'action_name': 'recommend_champion_lane', 'utterance': ['NAME_OPPONENT_CHAMPION', 'NAME_LANE'], 'backend': 'RECOMMENDED_CHAMPION',
    #  'function' :
    #  },
    #
	# {'action_name': 'recommend_champion_opponent', 'utterance': ['NAME_OPPONENT_CHAMPION', 'NAME_LANE'], 'backend': ['RECOMMENDED_CHAMPION'],
    #  'function' :
    #  },
    #
	# {'action_name': 'recommend_champion_default', 'utterance': ['NAME_OPPONENT_CHAMPION', 'NAME_LANE'], 'backend': ['RECOMMENDED_CHAMPION'],
    #  'function' :
    #  },
    #
	# {'action_name': 'recommend.item.specific_core', 'utterance': ['NAME_CHAMPION_FOR_ITEM', 'NAME_NUMBER_ITEM_CORE'], 'backend': ['RECOMMENDED_ITEM_1ST', 'RECOMMENDED_ITEM_2ST',
	# 																															  'RECOMMENDED_ITEM_3ST', 'RECOMMENDED_ITEM_4ST',
	# 																															  'RECOMMENDED_ITEM_5ST', 'RECOMMENDED_ITEM_6ST', 'RECOMMENDED_ITEM_SPECIFIC'],
    #  'function' :
    #  },
    #
	# {'action_name': 'recommend.item.all', 'utterance':['NAME_CHAMPION_FOR_ITEM', 'NAME_NUMBER_ITEM_CORE'], 'backend': ['RECOMMENDED_ITEM_1ST', 'RECOMMENDED_ITEM_2ST',
	# 																															  'RECOMMENDED_ITEM_3ST', 'RECOMMENDED_ITEM_4ST',
	# 																															  'RECOMMENDED_ITEM_5ST', 'RECOMMENDED_ITEM_6ST',]},
	# {'action_name': 'recommend.skill.specific', 'utterance':['NAME_CHAMPION', 'NAME_LEVEL'], 'backend': ['RECOMMENDED_SKILL_1ST', 'RECOMMENDED_SKILL_2ST', 'RECOMMENDED_SKILL_3ST', 'RECOMMENDED_SKILL_SPECIFIC'],
    #  'function' :
    #  },
    #
	# {'action_name': 'recommend.skill.all', 'utterance': ['NAME_CHAMPION', 'NAME_LEVEL'], 'backend': ['RECOMMENDED_SKILL_1ST', 'RECOMMENDED_SKILL_2ST', 'RECOMMENDED_SKILL_3ST', 'RECOMMENDED_SKILL_SPECIFIC'],
    #  'function' :
    #  },
    #
	# {'action_name': 'write.used_spell', 'utterance': ['NAME_CHAMPION_FOR_SPELL_RECORD', 'NAME_USED_SPELL'], 'backend': [],
    #  'function' :
    #  }
]

def find_function_in_query(utterance):
    for index, dict in enumerate(query_config):

        if len(dict['utterance']) == len(utterance.keys()):
            flag = True
            for param in utterance.keys():
                if param not in dict['utterance']:
                    flag = False
            if flag :
                return index

def answer(query):
    actionName, utterance = query['action']['actionName'], query['action']['parameters']
    idx = find_function_in_query(utterance)
    print(idx)
    print(utterance)
    return_from_function = query_config[idx]['function'](query_config[idx]['args'])

    result_dict = {'version': '2.0',
		'resultCode': 'OK',
		'output': {
			}}

    for backend_parameter in query_config[idx]['backend']:
        result_dict['output'][backend_parameter] = return_from_function[backend_parameter]
    print(result_dict)
    return result_dict

req = {'action': {'actionName': 'answer.opponent', 'parameters':{'NAME_OPPONENT_CHAMPION_FOR_ANALYSIS': {'type': 'NAME_CHAMPION', 'value': '애쉬'}}}}
req_2 = {'action': {'actionName': 'answer.opponent', 'parameters':{}}}
answer(req_2)
