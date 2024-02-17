from dataclasses import dataclass
from functools import total_ordering

from base import Solution


class Day05a(Solution):

  def solve(self, lines):

    (seed_to_location, _) = Almanac.parse(lines).resolve()
    import json; print(json.dumps(seed_to_location, indent=4))
    for nums in (seed_to_location.keys(), seed_to_location.values()):
      print(' '.join(str(num).zfill(2) for num in nums))
    return min(seed_to_location.values())


@total_ordering
@dataclass
class Entry:

  src_start: int
  dst_start: int
  length: int

  @classmethod
  def parse(cls, line):

    (dst, src, length) = map(int, line.split())
    return Entry(src, dst, length)

  def __contains__(self, num):

    return self.src_start <= num < self.src_start + self.length

  def __getitem__(self, num):

    return self.dst_start + num - self.src_start

  def __eq__(self, other):

    if isinstance(other, Entry):
      other = other.src_start
    return self.src_start == other

  def __lt__(self, other):

    if isinstance(other, Entry):
      other = other.src_start
    return self.src_start < other


@dataclass
class Map:

  source: str
  destination: str
  ranges: list[tuple]

  @classmethod
  def parse(cls, lines):

    (src, dst) = lines[0].split()[0].split('-to-')
    ranges = sorted(Entry.parse(line) for line in lines[1:])

    return cls(src, dst, ranges)

  def __getitem__(self, num):

    (left, right) = (0, len(self.ranges))
    while right > left:
      mid = int((left + right) / 2)
      if self.ranges[mid] > num:
        right = mid
      else:
        left = mid + 1
    closest = self.ranges[right - 1]

    if num in closest:
      return closest[num]
    return num


@dataclass
class Almanac:

  START = 'seed'

  seeds: list[int]
  maps: dict[Map]

  @classmethod
  def parse(cls, lines):

    seeds = [int(seed) for seed in lines[0].split()[1:]]

    maps = {}
    current = []
    for line in lines[1:] + ['']:
      if not line:
        if current:
          map = Map.parse(current)
          maps[map.source] = map
          current = []
      else:
        current.append(line)

    return Almanac(seeds, maps)

  def resolve(self):

    result = {}

    for seed in self.seeds:
      (cur_name, cur_id) = (self.START, seed)

      while (next_map := self.maps.get(cur_name)):
        (cur_name, cur_id) = (next_map.destination, next_map[cur_id])

      result[seed] = cur_id

    return (result, cur_name)
