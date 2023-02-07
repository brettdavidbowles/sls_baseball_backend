class Player:
  def __init__(self, id, name, team, composure, endurance, intellect, reflexes, speed, strength, willpower):
    self.id = id
    self.name = name
    self.team = team
    self.attributes = {
      'composure': composure,
      'endurance': endurance,
      'intellect': intellect,
      'reflexes': reflexes,
      'speed': speed,
      'strength': strength,
      'willpower': willpower
    }