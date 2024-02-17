from dataclasses import dataclass

from base import Solution


class Day04a(Solution):

  def solve(self, lines):

    return sum(Card.parse(line).points() for line in lines)


@dataclass
class Card:

  id: int
  nums_win: set[int]
  nums: set[int]

  @classmethod
  def parse(cls, s):

    (id, nums) = s.split(': ')
    id = int(id.split()[-1])
    nums = [set(map(int, n.split())) for n in nums.split(' | ')]

    return Card(id, *nums)

  def matches(self):

    return len(self.nums_win & self.nums)

  def points(self):

    matches = self.matches()
    return 2 ** (matches - 1) if matches else 0
