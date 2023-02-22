from django.core.management.base import BaseCommand, CommandError
from baseball.models import Game, Lineup, AtBat, LeftOnRunner
from baseball.sim.game import play_ball
import datetime

class Command(BaseCommand):
    help = 'Runs the baseball simulation'

    def handle(self, *args, **options):
        current_time = datetime.datetime.now()
        games_to_run = Game.objects.filter(date__hour=current_time.hour, date__day=current_time.day)

        for game in games_to_run:
          home_team_lineup = Lineup.objects.select_related('game').get(game=game, team=game.home_team).players.all().order_by('batting_order_number')
          mapped_home_team_lineup = [{ **p.player.__dict__, 'attributes': { **p.player.attributes.__dict__} } for p in home_team_lineup]
          away_team_lineup = Lineup.objects.select_related('game').get(game=game, team=game.away_team).players.all().order_by('batting_order_number')
          mapped_away_team_lineup = [{ **p.player.__dict__, 'attributes': { **p.player.attributes.__dict__} } for p in away_team_lineup]
          all_game_players = home_team_lineup | away_team_lineup

          home_team_pitcher = mapped_home_team_lineup[0]
          away_team_pitcher = mapped_away_team_lineup[0]
          home_team_batters = mapped_home_team_lineup[1:]
          away_team_batters = mapped_away_team_lineup[1:]
          raw_at_bat_list = play_ball(home_team_batters, home_team_pitcher, away_team_batters, away_team_pitcher)['at_bat_list']

          mapped_at_bats = [ AtBat(
            game=game,
            pitcher=all_game_players.get(player_id=atbat['pitcher_id']).player,
            batter=all_game_players.get(player_id=atbat['batter_id']).player,
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
                  player=all_game_players.get(player_id=runner['id']).player,
                  base=index + 1,
                  at_bat_subindex=0
                  # update when stolen bases become possible
                ))
          LeftOnRunner.objects.bulk_create(mapped_runners_left_on)
