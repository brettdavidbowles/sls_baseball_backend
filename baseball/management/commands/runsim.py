from django.core.management.base import BaseCommand, CommandError
from baseball.models import Game, Lineup, AtBat, LeftOnRunner, LineupPlayer, Player
from baseball.sim.game import play_ball
from baseball.constants import positions
import datetime

class Command(BaseCommand):
    help = 'Runs the baseball simulation'

    def handle(self, *args, **options):
        current_time = datetime.datetime.now()
        games_to_run = Game.objects.filter(date_time__hour=current_time.hour, date_time__day=current_time.day)
        for game in games_to_run:
          if game.at_bats.exists():
            continue
          
          try:
            home_team_lineup = Lineup.objects.select_related('game').get(game=game, team=game.home_team).players.all().order_by('batting_order_number')
          except Lineup.DoesNotExist:
            try:
              home_team_lineup = Lineup.objects.select_related('team').filter(team=game.home_team).order_by('game__date_time').last().players.all().order_by('batting_order_number')
              new_home_lineup = Lineup(game=game, team=game.home_team)
              new_home_lineup.save()
              new_home_team_lineup_players = []
              for player in home_team_lineup:
                new_home_team_lineup_players.append(LineupPlayer(
                  lineup=new_home_lineup,
                  player=player.player,
                  position=player.position,
                  batting_order_number=player.batting_order_number
                ))
              LineupPlayer.objects.bulk_create(new_home_team_lineup_players)
            except AttributeError:
              home_team_lineup = []
              new_home_lineup = Lineup(game=game, team=game.home_team)
              new_home_lineup.save()
              new_home_team_lineup_players = Player.objects.select_related('team').filter(team=game.home_team)[0:10]
              for index, player in enumerate(new_home_team_lineup_players):
                home_team_lineup.append(LineupPlayer(
                  lineup=new_home_lineup,
                  player=player,
                  position=positions[index],
                  batting_order_number=index
                ))
              LineupPlayer.objects.bulk_create(home_team_lineup)
          mapped_home_team_lineup = [{ **p.player.__dict__, 'attributes': { **p.player.attributes.__dict__} } for p in home_team_lineup]

          try:
            away_team_lineup = Lineup.objects.select_related('game').get(game=game, team=game.away_team).players.all().order_by('batting_order_number')
          except Lineup.DoesNotExist:
            try:
              away_team_lineup = Lineup.objects.select_related('team').filter(team=game.away_team).order_by('game__date_time').last().players.all().order_by('batting_order_number')
              new_away_lineup = Lineup(game=game, team=game.away_team)
              new_away_lineup.save()
              new_away_team_lineup_players = []
              for player in away_team_lineup:
                new_away_team_lineup_players.append(LineupPlayer(
                  lineup=new_away_lineup,
                  player=player.player,
                  position=player.position,
                  batting_order_number=player.batting_order_number
                ))
              LineupPlayer.objects.bulk_create(new_away_team_lineup_players)
            except AttributeError:
              away_team_lineup = []
              new_away_lineup = Lineup(game=game, team=game.away_team)
              new_away_lineup.save()
              new_away_team_lineup_players = Player.objects.select_related('team').filter(team=game.away_team)[0:10]
              for index, player in enumerate(new_away_team_lineup_players):
                away_team_lineup.append(LineupPlayer(
                  lineup=new_away_lineup,
                  player=player,
                  position=positions[index],
                  batting_order_number=index
                ))
              LineupPlayer.objects.bulk_create(away_team_lineup)
          mapped_away_team_lineup = [{ **p.player.__dict__, 'attributes': { **p.player.attributes.__dict__} } for p in away_team_lineup]
          
          home_team_set = set(list(home_team_lineup))
          away_team_set = set(list(away_team_lineup))
          all_game_players = list(home_team_set.union(away_team_set))

          home_team_pitcher = mapped_home_team_lineup[0]
          away_team_pitcher = mapped_away_team_lineup[0]
          home_team_batters = mapped_home_team_lineup[1:]
          away_team_batters = mapped_away_team_lineup[1:]
          raw_at_bat_list = play_ball(home_team_batters, home_team_pitcher, away_team_batters, away_team_pitcher)['at_bat_list']

          mapped_at_bats = [ AtBat(
            game=game,
            pitcher=next(player for player in all_game_players if player.player_id == atbat['pitcher_id']).player,
            batter=next(player for player in all_game_players if player.player_id == atbat['batter_id']).player,
            inning=atbat['inning'],
            strikes=atbat['strikes'],
            balls=atbat['balls'],
            rbis=atbat['rbis'],
            outcome=atbat['outcome'],
            game_at_bat_number=atbat['game_at_bat_number']
          ) for atbat in raw_at_bat_list]
          AtBat.objects.bulk_create(mapped_at_bats)
          mapped_runners_left_on = []
          for atbat in raw_at_bat_list:
            for index, runner in enumerate(atbat['new_runners_on']):
              if runner:
                mapped_runners_left_on.append(LeftOnRunner(
                  at_bat=AtBat.objects.get(game__id=game.id, game_at_bat_number=atbat['game_at_bat_number']),
                  player = next(player for player in all_game_players if player.player_id == runner['id']).player,
                  base=index + 1,
                  at_bat_subindex=0
                  # update when stolen bases become possible
                ))
          LeftOnRunner.objects.bulk_create(mapped_runners_left_on)
