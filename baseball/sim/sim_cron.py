import datetime
from django.utils import timezone
from baseball.models import Game, Lineup, AtBat, Player, LeftOnRunner
from baseball.sim.game import play_ball

current_time = datetime.datetime.now()
games_to_run = Game.objects.filter(date__hour=current_time.hour, date__day=current_time.day)

for game in games_to_run:
  home_team_lineup = Lineup.objects.select_related('game').get(game=game, team=game.home_team).players.all().order_by('batting_order_number')
  mapped_home_team_lineup = [{ **p.player.__dict__, 'attributes': { **p.player.attributes.__dict__} } for p in home_team_lineup]
  away_team_lineup = Lineup.objects.select_related('game').get(game=game, team=game.away_team).players.all().order_by('batting_order_number')
  mapped_away_team_lineup = [{ **p.player.__dict__, 'attributes': { **p.player.attributes.__dict__} } for p in away_team_lineup]

  home_team_pitcher = mapped_home_team_lineup[0]
  away_team_pitcher = mapped_away_team_lineup[0]
  home_team_batters = mapped_home_team_lineup[1:]
  away_team_batters = mapped_away_team_lineup[1:]
  print(home_team_pitcher['attributes'])
  raw_at_bat_list = play_ball(home_team_batters, home_team_pitcher, away_team_batters, away_team_pitcher)['at_bat_list']

  at_bats = [AtBat()]
  # AtBat.objects.create(
  #   game=Game.objects.get(id=1),
  #   pitcher=Player.objects.get(first_name='ghostface'),
  #   batter=Player.objects.get(first_name='dirt'),
  #   inning=1,
  #   strikes=0,
  #   balls=0,
  #   rbis=0,
  #   outcome='single',
  #   game_at_bat_number=1
  # )
  LeftOnRunner.objects.create(
    at_bat=AtBat.objects.get(game__id=game.id, game_at_bat_number=1),


# print(games_to_run[0])
# print(Lineup.objects.filter(game=games_to_run[0]))
# def find_games(date)