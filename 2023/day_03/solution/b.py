from collections import defaultdict
from dataclasses import dataclass

from a import Day03a, Part, Schematic


class Day03b(Day03a):

  SOLUTION = 82301120

  def solve(self, lines):

    return sum(gear.ratio() for gear in SchematicB.parse(lines))


class SchematicB(Schematic):

  GEAR = '*'

  def __iter__(self):

    parts_near_gears = defaultdict(lambda: [])
    for part in self.parts:
      for symbol in self.adjacent_symbols(part, None, SchematicB.GEAR):
        parts_near_gears[symbol].append(part)

    for parts in parts_near_gears.values():
      if len(parts) == 2:
        yield Gear(*parts)


@dataclass
class Gear:

  part1: Part
  part2: Part

  def ratio(self):

    return self.part1.number * self.part2.number
