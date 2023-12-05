from base import Solution


class Day01a(Solution):

  SOLUTION = 54601

  def solve(self, lines):

    return sum(self.decode(line) for line in lines)

  def decode(self, line):

    result = []
    for reverse in (False, True):
      result.append(self.first_num(line, reverse))

    return int(''.join(result))

  def first_num(self, line, reverse=False):

    if reverse:
      line = reversed(line)

    for c in line:
      if c.isdigit():
        return c
