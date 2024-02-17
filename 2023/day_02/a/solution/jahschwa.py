from collections import defaultdict
from enum import Enum, auto

from base import Solution


class Day02a(Solution):

  def __init__(self):

    self.cubes = {
      Color.red: 12,
      Color.green: 13,
      Color.blue: 14,
    }

  def solve(self, lines):

    result = 0
    for line in lines:
      if self.cubes in (game := Game.parse(line)):
        result += game.id

    return result


class Color(Enum):

  red = auto()
  green = auto()
  blue = auto()


class Game:

  def __init__(self, id, cubes):

    self.id = id
    self.min_cubes = cubes

  @classmethod
  def parse(cls, s):

    (id, rounds) = s.split(': ')
    id = int(id.split()[-1])

    cubes = defaultdict(lambda: 0)
    for round in rounds.split('; '):
      for (color, count) in Game.parse_round(round).items():
        cubes[color] = max(cubes[color], count)

    return cls(id, cubes)

  @staticmethod
  def parse_round(s):

    cubes = {}
    for cube in s.split(', '):
      (count, color) = cube.split()
      cubes[Color[color]] = int(count)

    return cubes

  def __contains__(self, round):

    return all(
      self.min_cubes[color] <= count
      for (color, count) in round.items()
    )
