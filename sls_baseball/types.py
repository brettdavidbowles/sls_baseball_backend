import strawberry
from baseball import models
from typing import List
from strawberry import auto


@strawberry.django.type(models.User)
class User:
    pass

@strawberry.django.type(models.Player)
class Player:
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
    name: auto
    location: auto
    stadium: auto
    league: 'League'
    games: List['Game']

@strawberry.django.type(models.League)
class League:
    name: auto

@strawberry.django.type(models.Manager)
class Manager:
    first_name: auto
    last_name: auto
    team: 'Team'

@strawberry.django.type(models.Season)
class Season:
    name: auto
    start_date: auto
    end_date: auto

@strawberry.django.type(models.Game)
class Game:
    date: auto
    home_team: Team
    away_team: Team
    leauge: League
    season: Season
    at_bats: List['AtBat']
    lineups: List['Lineup']

@strawberry.django.type(models.Lineup)
class Lineup:
    game: 'Game'
    team: Team
    players: List['LineupPlayer']

@strawberry.django.type(models.LineupPlayer)
class LineupPlayer:
    lineup: Lineup
    player: Player
    position: auto
    batting_order_number: auto

@strawberry.django.type(models.AtBat)
class AtBat:
    player: Player
    inning: auto
    strikes: auto
    balls: auto
    rbis: auto
    outcome: auto
    left_on_runners: List['LeftOnRunner']

@strawberry.django.type(models.LeftOnRunner)
class LeftOnRunner:
    player: Player
    base: auto
    at_bat_subindex: auto

@strawberry.django.type(models.ScheduledGame)
class ScheduledGame:
    date: auto
    home_team: Team
    away_team: Team
    leauge: League