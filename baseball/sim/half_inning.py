from ..utility_functions import find_next_batter_index
from ..classes import Player
from .at_bat import at_bat
from ..constants import AT_BAT_OUTCOMES

def half_inning(lineup, place_in_lineup, pitcher, team_at_bats, half_inning, opponent_at_bats):
  runners_on = [False, False, False]
  runs = 0
  hits = 0
  errors = 0
  outs = 0
  total_team_at_bats = team_at_bats
  at_bat_list = []
  place_in_lineup_counter = place_in_lineup
  while outs < 3:
    current_at_bat = at_bat(lineup[place_in_lineup_counter], pitcher, runners_on)
    total_team_at_bats += 1
    at_bat_list.append({
      'team_at_bat': total_team_at_bats,
      **current_at_bat,
      'half_inning': half_inning,
      'game_at_bat_number': opponent_at_bats + total_team_at_bats
    })
    if current_at_bat['outcome'] in AT_BAT_OUTCOMES['out']:
      outs += 1
      place_in_lineup_counter = find_next_batter_index(place_in_lineup_counter)
    else:
      hits += 1
      runs += current_at_bat['rbis']
      runners_on = current_at_bat['new_runners_on'].copy()
      place_in_lineup_counter = find_next_batter_index(place_in_lineup_counter)
  return {
    'runs': runs,
    'hits': hits,
    'errors': errors,
    'place_in_lineup': place_in_lineup_counter,
    'at_bat_list': at_bat_list,
    'total_team_at_bats': total_team_at_bats
  }