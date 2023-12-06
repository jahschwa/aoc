from functools import reduce
from operator import mul

from day_02a import Day02a, Game


class Day02b(Day02a):

  SOLUTION = 72970

  def solve(self, lines):

    return sum(GameB.parse(line).power() for line in lines)


class GameB(Game):

  def power(self):

    return reduce(mul, self.min_cubes.values())
