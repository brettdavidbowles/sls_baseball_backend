from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from .constants import AT_BAT_OUTCOMES
from django.db.models.signals import post_save
from django.dispatch import receiver
from .constants import positions


class User(AbstractUser):
    pass


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.ForeignKey(
        "Team", on_delete=models.SET_NULL, related_name="players", blank=True, null=True)
    at_bats = models.ManyToManyField(
        "AtBat", related_name="players", blank=True)
    # age = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PlayerAttribute(models.Model):
    player = models.OneToOneField(
        Player, on_delete=models.CASCADE, primary_key=True, related_name="attributes")
    composure = models.IntegerField()
    endurance = models.IntegerField()
    intellect = models.IntegerField()
    reflexes = models.IntegerField()
    speed = models.IntegerField()
    strength = models.IntegerField()
    willpower = models.IntegerField()

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} Attributes"


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    stadium = models.CharField(max_length=50, blank=True, null=True)
    league = models.ForeignKey(
        "League", on_delete=models.SET_NULL, related_name="teams", null=True)
    games = models.ManyToManyField("Game", blank=True)

    def __str__(self):
        return f"{self.name}"


class League(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Manager(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    team = models.ForeignKey(
        "Team", on_delete=models.SET_NULL, related_name="managers", null=True)
    user = models.ForeignKey(
        "User", on_delete=models.SET_NULL, related_name="managers", null=True)

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}: {self.team.name} Manager {self.id}"
        else:
            return f"{self.team.name} Manager {self.id}"


class Season(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    date_time = models.DateTimeField()
    league = models.ForeignKey(
        "League", on_delete=models.RESTRICT, related_name="games")
    season = models.ForeignKey(
        "Season", on_delete=models.RESTRICT, related_name="games")
    home_team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="home_games")
    away_team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="away_games")

    def __str__(self):
        return f"Game {self.id} on {self.date_time}"

    def home_team_total_runs(self):
        return self.at_bats.filter(batter__team=self.home_team).aggregate(Sum('rbis'))['rbis__sum']

    def away_team_total_runs(self):
        return self.at_bats.filter(batter__team=self.away_team).aggregate(Sum('rbis'))['rbis__sum']

    def home_team_total_hits(self):
        return self.at_bats.filter(batter__team=self.home_team, outcome__in=AT_BAT_OUTCOMES['hit']).count()

    def away_team_total_hits(self):
        return self.at_bats.filter(batter__team=self.away_team, outcome__in=AT_BAT_OUTCOMES['hit']).count()

    def home_team_total_errors(self):
        return self.at_bats.filter(batter__team=self.home_team).aggregate(Sum('errors'))['errors__sum']

    def away_team_total_errors(self):
        return self.at_bats.filter(batter__team=self.away_team).aggregate(Sum('errors'))['errors__sum']


def create_default_lineup(team, game):
    # need to account for traded players
    try:
        team_lineup = Lineup.objects.select_related('team').filter(team=team).order_by(
            'game__date_time').last().players.all().order_by('batting_order_number')
        new_lineup = Lineup(game=game, team=team)
        new_lineup.save()
        new_team_lineup_players = []
        for player in team_lineup:
            new_team_lineup_players.append(LineupPlayer(
                lineup=new_lineup,
                player=player.player,
                position=player.position,
                batting_order_number=player.batting_order_number
            ))
        LineupPlayer.objects.bulk_create(new_team_lineup_players)
    except AttributeError:
        team_lineup = []
        new_lineup = Lineup(game=game, team=team)
        new_lineup.save()
        new_team_lineup_players = Player.objects.select_related(
            'team').filter(team=team)[0:10]
        for index, player in enumerate(new_team_lineup_players):
            team_lineup.append(LineupPlayer(
                lineup=new_lineup,
                player=player,
                position=positions[index],
                batting_order_number=index
            ))
        LineupPlayer.objects.bulk_create(team_lineup)


@receiver(post_save, sender=Game)
def create_lineups(sender, instance, created, **kwargs):
    if created:
        create_default_lineup(instance.home_team, instance)
        create_default_lineup(instance.away_team, instance)


class HalfInning(models.Model):
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="half_innings")
    inning = models.IntegerField()
    home_team_at_bat = models.BooleanField()

    def __str__(self):
        if self.home_team_at_bat:
            return f"Bottom of {self.inning} Inning of Game {self.game.id}"
        else:
            return f"Top of {self.inning} Inning of Game {self.game.id}"

    @property
    def rbis(self):
        return self.at_bats.aggregate(Sum('rbis'))['rbis__sum'] or 0

    @property
    def hits(self):
        return self.at_bats.filter(outcome__in=AT_BAT_OUTCOMES['hit']).count()

    @property
    def errors(self):
        return self.at_bats.aggregate(Sum('errors'))['errors__sum'] or 0


class Lineup(models.Model):
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="lineups")
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="lineups")

    def __str__(self):
        return f"{self.team.name} Lineup for Game {self.game.id}"


class LineupPlayer(models.Model):
    lineup = models.ForeignKey(
        "Lineup", on_delete=models.CASCADE, related_name="players")
    player = models.ForeignKey(
        "Player", on_delete=models.CASCADE, related_name="lineups")
    position = models.CharField(max_length=50)
    batting_order_number = models.IntegerField()

    def __str__(self):
        return f"{self.batting_order_number} in {self.lineup.team.name} lineup for Game {self.lineup.game.id}"


class AtBat(models.Model):
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="at_bats")
    pitcher = models.ForeignKey(
        "Player", on_delete=models.RESTRICT, related_name="pitched_at_bats")
    batter = models.ForeignKey(
        "Player", on_delete=models.RESTRICT, related_name="batted_at_bats")
    half_inning = models.ForeignKey(
        "HalfInning", on_delete=models.CASCADE, related_name="at_bats")
    strikes = models.IntegerField()
    balls = models.IntegerField()
    rbis = models.IntegerField()
    outcome = models.CharField(max_length=50)
    game_at_bat_number = models.IntegerField()
    errors = models.IntegerField(default=0)

    def __str__(self):
        return f"At bat {self.game_at_bat_number} in Game {self.game.id}"


class LeftOnRunner(models.Model):
    default_runner = {
        "first_name": "default",
        "last_name": "runner",
    }
    at_bat = models.ForeignKey(
        "AtBat", on_delete=models.CASCADE, related_name="runners_left_on_base")
    player = models.ForeignKey(
        "Player", default=default_runner, on_delete=models.SET_DEFAULT)
    base = models.IntegerField()
    # this is if an at bat has stolen bases, thus multiple scenarios. i hate the name and hate that i need this comment but i'm drawing a blank
    at_bat_subindex = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} left on base {self.base} in Game {self.at_bat.game.id}"

# class ScheduledGame(models.Model):
#     date = models.DateTimeField()
#     home_team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="home_scheduled_games")
#     away_team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="away_scheduled_games")
#     leauge = models.ForeignKey("League", on_delete=models.SET_NULL, related_name="scheduled_games", null=True)

#     def __str__(self):
#         return f"Game on {self.scheduled_date}: {self.away_team} at {self.home_team}"
