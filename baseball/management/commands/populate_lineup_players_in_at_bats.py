from baseball.models import AtBat, LineupPlayer, Player
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        at_bats = AtBat.objects.all()
        for at_bat in at_bats:
            game = at_bat.game
            batter = at_bat.batter
            pitcher = at_bat.pitcher
            lineup_batter = LineupPlayer.objects.filter(
                lineup__game=game, player=batter)
            lineup_pitcher = LineupPlayer.objects.filter(
                lineup__game=game, player=pitcher)
            AtBat.objects.filter(pk=at_bat.pk).update(
                lineup_batter=lineup_batter[0], lineup_pitcher=lineup_pitcher[0])
