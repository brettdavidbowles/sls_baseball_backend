from .half_inning import half_inning
from .classes import Player
from .utility_functions import find_next_batter_index, create_random_pitcher_and_lineup

def play_ball(home_lineup, home_pitcher, away_lineup, away_pitcher):
  scoreboard = {
    'home_team': {
      'runs': 0,
      'hits': 0,
      'errors': 0,
      'at_bats': 0
    },
    'away_team': {
      'runs': 0,
      'hits': 0,
      'errors': 0,
      'at_bats': 0
    },
    'inning': 1,
  }
  home_place_in_lineup = 0
  away_place_in_lineup = 0
  stats_list = []
  at_bat_list = []
  trys = 0
  while trys < 20 and (scoreboard['inning'] < 10 or scoreboard['home_team']['runs'] == scoreboard['away_team']['runs']):
    trys += 1
    # this is dumb i don't like it, but it's late... do a try catch instead
    if scoreboard['inning'] > 14:
      return play_ball(home_lineup, home_pitcher, away_lineup, away_pitcher)
    # this is a temp hack to avoid games going into an absurd amount of innings
    away_bats = half_inning(away_lineup, away_place_in_lineup, home_pitcher, scoreboard['away_team']['at_bats'], scoreboard['inning'], scoreboard['home_team']['at_bats'])
    scoreboard['away_team']['runs'] += away_bats['runs']
    scoreboard['away_team']['hits'] += away_bats['hits']
    scoreboard['away_team']['errors'] += away_bats['errors']
    scoreboard['away_team']['at_bats'] = away_bats['total_team_at_bats']
    away_place_in_lineup = find_next_batter_index(away_bats['place_in_lineup'])
    at_bat_list.extend(away_bats['at_bat_list'])
    # this could probably be more explicit with what inning
    if scoreboard['inning'] < 9 or scoreboard['home_team']['runs'] <= scoreboard['away_team']['runs']:
      home_bats = half_inning(home_lineup, home_place_in_lineup, away_pitcher, scoreboard['home_team']['at_bats'], scoreboard['inning'], scoreboard['away_team']['at_bats'])
      scoreboard['home_team']['runs'] += home_bats['runs']
      scoreboard['home_team']['hits'] += home_bats['hits']
      scoreboard['home_team']['errors'] += home_bats['errors']
      scoreboard['home_team']['at_bats'] = home_bats['total_team_at_bats']
      home_place_in_lineup = find_next_batter_index(home_bats['place_in_lineup'])
      at_bat_list.extend(home_bats['at_bat_list'])
      stats_list.append({
        'inning': scoreboard['inning'],
        'away_runs': scoreboard['away_team']['runs'],
        'home_runs': scoreboard['home_team']['runs']
      })
    else:
      stats_list.append({
        'inning': scoreboard['inning'],
        'away_runs': scoreboard['away_team']['runs']
      })
    scoreboard['inning'] += 1
  scoreboard['inning'] -= 1
  return {
    'at_bat_list': at_bat_list,
    # 'stats_list': stats_list
  }

# bza = create_random_pitcher_and_lineup('bza ballers')
# bza_pitcher = bza[0]
# bza_lineup = bza[1:]
# warly = create_random_pitcher_and_lineup('warly warriors')
# warly_pitcher = warly[0]
# warly_lineup = warly[1:]
# print(play_ball(bza_lineup, bza_pitcher, warly_lineup, warly_pitcher))

