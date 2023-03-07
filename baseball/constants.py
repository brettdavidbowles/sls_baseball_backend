ATTRIBUTES = { 'strength', 'speed', 'endurance', 'composure', 'reflexes', 'intellect', 'willpower' }

BATTING_AVERAGE_ATTRIBUTES = [
  {
    'name': 'strength',
    'weight': .3
  },
  {
    'name': 'composure',
    'weight': .4
  },
  {
    'name': 'intellect',
    'weight': .3
  }
]

# WHIP = Walks + Hits / Innings Pitched
WHIP_ATTRIBUTES = [
  {
    'name': 'strength',
    'weight': .3
  },
  {
    'name': 'composure',
    'weight': .4
  },
  {
    'name': 'intellect',
    'weight': .3
  }
]

SLUGGING_PERCENTAGE_ATTRIBUTES = [
  {
    'name': 'strength',
    'weight': 1
  }
]

AT_BAT_OUTCOMES = {
  'hit': ( 'single', 'double', 'triple', 'homerun' ),
  'out': ( 'strikeout', 'fieldout' ),
  'neither_hit_nor_out': ( 'walk', 'hit_by_pitch' )
}

positions = [
  'pitcher', 'catcher', 'first_base', 'second_base', 'third_base', 'shortstop', 'left_field', 'center_field', 'right_field', 'designated_hitter'
]