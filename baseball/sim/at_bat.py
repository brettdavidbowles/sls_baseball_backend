from .classes import Player
from .constants import BATTING_AVERAGE_ATTRIBUTES, WHIP_ATTRIBUTES, SLUGGING_PERCENTAGE_ATTRIBUTES
from .utility_functions import find_attributes_and_apply_weights, random_pitch_count, run_bases
from random import random
from operator import itemgetter

def at_bat(batter, pitcher, runners_on):
  at_bat_random = random()
  # fix all of this shit, just translating to python right now
  batter_advantage = find_attributes_and_apply_weights(batter, BATTING_AVERAGE_ATTRIBUTES)
  pitcher_advantage = find_attributes_and_apply_weights(pitcher, WHIP_ATTRIBUTES)
  # need pitcher fatique function, add at_bats as parameter
  hit_calculation = at_bat_random - batter_advantage + pitcher_advantage
  if hit_calculation < .2:
    strikes, balls = itemgetter('strikes', 'balls')(random_pitch_count(False, False))
    slugging_random = random()
    # slugging_probability = slugging_random * find_attributes_and_apply_weights(batter, SLUGGING_PERCENTAGE_ATTRIBUTES)
    # do this later it's messing up with the dummy data
    slugging_probability = slugging_random
    if slugging_probability > .8:
      outcome = 'homerun'
    elif slugging_probability > .65:
      outcome = 'triple'
    elif slugging_probability > .5:
      outcome = 'double'
    else:
      outcome = 'single'
  else:
    strikes, balls = itemgetter('strikes', 'balls')(random_pitch_count(True, False))
    outcome = 'strikeout'
  new_runners_on, rbis = itemgetter('new_runners_on', 'rbis')(run_bases(outcome, batter, runners_on))
  return {
    'outcome': outcome,
    'strikes': strikes,
    'balls': balls,
    'new_runners_on': new_runners_on,
    'rbis': rbis,
    'batter_id': batter['id'],
    'pitcher_id': pitcher['id']
  }
