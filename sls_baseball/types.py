import strawberry
from baseball import models
from typing import List
from strawberry import auto
import datetime


@strawberry.django.type(models.User)
class User:
    pass

@strawberry.django.type(models.Player)
class Player:
    id: auto
    first_name: auto
    last_name: auto
    team: 'Team'
    at_bats: List['AtBat']
    @strawberry.django.field
    def attributes(self, info) -> 'PlayerAttribute':
        return models.PlayerAttribute.objects.get(player__id=self.id)

@strawberry.django.type(models.PlayerAttribute)
class PlayerAttribute:
    composure: auto
    endurance: auto
    intellect: auto
    reflexes: auto
    speed: auto
    strength: auto
    willpower: auto

@strawberry.django.type(models.Team)
class Team:
    id: auto
    name: auto
    location: auto
    stadium: auto
    league: 'League'
    games: List['Game']

@strawberry.django.type(models.League)
class League:
    id: auto
    name: auto

@strawberry.django.type(models.Manager)
class Manager:
    id: auto
    first_name: auto
    last_name: auto
    team: 'Team'

@strawberry.django.type(models.Season)
class Season:
    id: auto
    name: auto
    start_date: auto
    end_date: auto

@strawberry.django.type(models.HalfInning)
class HalfInning:
    id: auto
    inning: auto
    at_bats: List['AtBat']
    game: 'Game'
    home_team_at_bat: auto
    rbis: int
    hits: int
    errors: int

@strawberry.django.filters.filter(models.Game)
class GameFilter:
    id: auto
    is_past: bool or None
    def filter_is_past(self, queryset):
        if self.is_past is None:
            return queryset.order_by('date_time')
        if self.is_past:
            return queryset.filter(date_time__lte=datetime.datetime.now()).order_by('-date_time')
        else:
            return queryset.filter(date_time__gt=datetime.datetime.now()).order_by('date_time')


@strawberry.django.type(models.Game, pagination=True, filters=GameFilter)
class Game:
    id: auto
    date_time: auto
    home_team: Team
    away_team: Team
    league: League
    season: Season
    at_bats: List['AtBat']
    lineups: List['Lineup']
    half_innings: List['HalfInning']
    home_team_total_runs: int
    away_team_total_runs: int
    home_team_total_hits: int
    away_team_total_hits: int
    home_team_total_errors: int
    away_team_total_errors: int

@strawberry.django.type(models.Lineup)
class Lineup:
    id: auto
    game: 'Game'
    team: Team
    players: List['LineupPlayer']

@strawberry.django.type(models.LineupPlayer)
class LineupPlayer:
    id: auto
    lineup: Lineup
    player: Player
    position: auto
    batting_order_number: auto

@strawberry.django.type(models.AtBat)
class AtBat:
    id: auto
    pitcher: Player
    batter: Player
    half_inning: HalfInning
    strikes: auto
    balls: auto
    errors: auto
    rbis: auto
    outcome: auto
    left_on_runners: List['LeftOnRunner']
    game_at_bat_number: auto
    game: Game

@strawberry.django.type(models.LeftOnRunner)
class LeftOnRunner:
    id: auto
    player: Player
    base: auto
    at_bat_subindex: auto

# @strawberry.django.type(models.ScheduledGame)
# class ScheduledGame:
#     date: auto
#     home_team: Team
#     away_team: Team
#     leauge: League
