from collections import defaultdict

from day_04a import Card, Day04a


class Day04b(Day04a):

  SOLUTION = 12263631

  def solve(self, lines):

    cards = defaultdict(lambda: 1)
    cards[0] = 1

    for (idx, line) in enumerate(lines):
      copies = cards[idx]
      points = Card.parse(line).matches()
      for copy in range(idx + 1, idx + 1 + points):
        cards[copy] += copies

    return sum(cards.values())
