from crawling.riot_api import *
import sys



query_config =[
	{'action_name': 'answer.opponent.specific', 'utterance' : ['NAME_OPPONENT_CHAMPION_FOR_ANALYSIS'] , 'backend': ['OPPONENT_CHAMPION_WINNING_RATE', 'OPPONENT_CHAMPION_TEAR'],
     'function' : Specific_PlayerSummary
     },
	{'action_name': 'answer.opponent.caution_champion', 'utterance': [], 'backend': ['OPPONENT_CAUTION_CHAMPION', 'OPPONENT_CHAMPION_WINNING_RATE', 'OPPONENT_CHAMPION_TEAR'],
     'function' : Total_PlayerSummary
     },
    # spell cooltime
	{'action_name': 'answer.spell.specific_champion.specific_spell', 'utterance': ['NAME_CHAMPION_FOR_SPELL', 'NAME_SPELL'] , 'backend': ['REMAINING_TIME_OF_SPELL'],
     'function' : AnswerSpellRemainingTime

     },
	# {'action_name': 'answer.spell.specific_champion.wo_specific_spell', 'utterance': ['NAME_CHAMPION_FOR_SPELL', 'NAME_SPELL'], 'backend':['USED_SPELL_NAMES', 'REMAINING_TIMES'],
    #  'function' : ,'args':
    #  },
    #
	# {'action_name': 'answer.spell.all', 'utterance': ['NAME_CHAMPION_FOR_SPELL', 'NAME_SPELL'], 'backend': ['OPPONENT_CHAMPION1', 'SEPLLS_CHAMPION1', 'REMAINING_TIME_CHAMPION1'],
    #  'function' :
    #  },

	{'action_name': 'recommend_champion_lane', 'utterance': ['NAME_OPPONENT_CHAMPION', 'NAME_LANE'], 'backend': ['RECOMMENDED_CHAMPION'],
     'function' : RecommendChampionFromLane
     },

	{'action_name': 'recommend_champion_opponent', 'utterance': ['NAME_OPPONENT_CHAMPION', 'NAME_LANE'], 'backend': ['RECOMMENDED_CHAMPION'],
     'function' :   RecommendChampionFromChampion
     },

	{'action_name': 'recommend_champion_default', 'utterance': ['NAME_OPPONENT_CHAMPION', 'NAME_LANE'], 'backend': ['RECOMMENDED_CHAMPION'],
     'function' :   RecommendRandomChampion
     },

	{'action_name': 'recommend.item.specific_core', 'utterance': ['NAME_CHAMPION_FOR_ITEM', 'NAME_NUMBER_ITEM_CORE'], 'backend': ['RECOMMENDED_ITEM_SPECIFIC'],
     'function' : RecommendItemSpecific
     },

	{'action_name': 'recommend.item.all', 'utterance':['NAME_CHAMPION_FOR_ITEM', 'NAME_NUMBER_ITEM_CORE'], 'backend': ['RECOMMENDED_ITEM_1ST', 'RECOMMENDED_ITEM_2ST',
																																  'RECOMMENDED_ITEM_3ST'],
    'function' : RecommendItemAll
     },

	{'action_name': 'recommend.skill.specific', 'utterance':['NAME_CHAMPION', 'NAME_LEVEL'], 'backend': ['RECOMMENDED_SKILL_SPECIFIC'],
     'function' : RecommendSkillSpecific
     },

	{'action_name': 'recommend.skill.all', 'utterance': ['NAME_CHAMPION', 'NAME_LEVEL'], 'backend': ['RECOMMENDED_SKILL_1ST', 'RECOMMENDED_SKILL_2ST', 'RECOMMENDED_SKILL_3ST'],
     'function' : RecommendSkillAll
     },

	{'action_name': 'write.used_spell', 'utterance': ['NAME_CHAMPION_FOR_SPELL_RECORD', 'NAME_USED_SPELL'], 'backend': [],
     'function' : RecordSpellTime
    }
]

def find_function_in_query(action):
    for index, dict in enumerate(query_config):
        if action == dict['action_name']:
            return index
    return -1

def answer(query, current_game):
    actionName, utterance = query['action']['actionName'], query['action']['parameters']
    idx = find_function_in_query(actionName)
    args = {}
    args['current_game'] = current_game
    if len(utterance) != 0:
        for keys in utterance.keys():
            args[keys] = query['action']['parameters'][keys]['value']

    # print(idx)
    # print(utterance)
    # print(args)

    if idx == -1:
        print("idx is -1")
        return {'version': '2.0',
		'resultCode': 'OK',
		'output': {
			}}

    return_from_function = query_config[idx]['function'](**args)

    result_dict = {'version': '2.0',
                   'resultCode': 'OK',
                   'output': {
                   }}

    for backend_parameter in query_config[idx]['backend']:
        result_dict['output'][backend_parameter] = return_from_function[backend_parameter]
    print(result_dict)
    return result_dict

    # if actionName == 'write.used_spell':
    #     current_game_new = RecordSpellTime(**args)
    #     return 1, result_dict, current_game_new
    # else:
    #     for backend_parameter in query_config[0]['backend']:
    #         result_dict['output'][backend_parameter] = return_from_function[backend_parameter]
    #     print(result_dict)
    # return 0, result_dict, current_game

req = {'action': {'actionName': 'answer.opponent', 'parameters':{'NAME_OPPONENT_CHAMPION_FOR_ANALYSIS': {'type': 'NAME_CHAMPION', 'value': '애쉬'}}}}
req_2 = {'action': {'actionName': 'answer.opponent', 'parameters':{}}}
# answer(req_2)
