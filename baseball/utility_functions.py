from random import random
from .constants import AT_BAT_OUTCOMES
from .classes import Player


def find_attributes_and_apply_weights(player, attribute_weight_dicts):
    relevant_attribute_weighted_values = []
    for attribute in attribute_weight_dicts:
        weighted_attribute = attribute['weight'] * \
            player['attributes'][attribute['name']]
        relevant_attribute_weighted_values.append(weighted_attribute)
    return sum(relevant_attribute_weighted_values) / 100


def random_pitch_count(is_strikeout, is_walk):
    strikes_random = random()
    balls_random = random()
    if is_walk:
        ball_count = 4
    elif balls_random < .25:
        ball_count = 0
    elif balls_random < .5:
        ball_count = 1
    elif balls_random < .75:
        ball_count = 2
    else:
        ball_count = 3

    if is_strikeout:
        strike_count = 3
    elif strikes_random < .1:
        strike_count = 0
    elif strikes_random < .5:
        strike_count = 1
    else:
        strike_count = 2

    return {
        'strikes': strike_count,
        'balls': ball_count
    }


def run_bases(hit, runner, runners_on):
    if hit in AT_BAT_OUTCOMES['out']:
        return {
            'rbis': 0,
            'new_runners_on': runners_on
        }
    else:
        new_runners_on = runners_on.copy()
        hit_index = AT_BAT_OUTCOMES['hit'].index(hit)
        rbis = 0
        for index, runner_on in enumerate(new_runners_on):
            if runner_on and index <= hit_index:
                new_runners_on[index] = False
                index + hit_index > 2
                if index + hit_index + 2 > 2:
                    rbis += 1
                else:
                    new_runners_on[index + hit_index + 2] = runner_on
        if hit == 'homerun':
            rbis += 1
        else:
            new_runners_on[hit_index] = runner
        return {
            'rbis': rbis,
            'new_runners_on': new_runners_on
        }


def find_next_batter_index(current_index):
    if current_index == 8:
        return 0
    else:
        return current_index + 1


def create_random_pitcher_and_lineup(team_name):
    lineup = []
    for i in range(10):
        lineup.append(Player(
            i,
            f'{team_name} Player {i}',
            team_name,
            random() * 100,
            random() * 100,
            random() * 100,
            random() * 100,
            random() * 100,
            random() * 100,
            random() * 100,
        ))
    return lineup


def isAHit(outcome):
    return outcome in AT_BAT_OUTCOMES['hit']
