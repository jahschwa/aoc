from dataclasses import dataclass, field
from math import floor, log
import time
from traceback import format_exc

from puzzle_input import PuzzleInput


RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
YELLOW = '\033[93m'


@dataclass
class Duration:

  start: float

  stop: float = field(default_factory=time.time)
  precision: int = 4
  width: int = 12

  elapsed: float = None

  _color: str = None
  _factor: int = None
  _scaled: float = None
  _unit: float = None


  def __post_init__(self):

    self.elapsed = self.stop - self.start

    power = floor(log(self.elapsed, 1000))
    self._factor = 1000 ** power
    self._scaled = self.elapsed / self._factor

    unit = 'smu'[-power]
    self._unit = 'sec' if unit == 's' else unit + 's '

    self._color = [RED, YELLOW, GREEN][-power]

  def __str__(self):

    return ('{}{:>8.%sf} {:<3}{}' % self.precision).format(
      self._color, self._scaled, self._unit, RESET
    )


@dataclass
class Result:

  elapsed: Duration
  expected: int
  input_name: str
  observed: int | str
  correct: None = None

  def __post_init__(self):

    self.correct = self.observed == self.expected


class Solution:

  def parse(self, line: str) -> str:

    return line

  def solve(self, lines: list[str]) -> int:

    raise NotImplementedError

  def _solve(self, puzzle_input: PuzzleInput) -> Result:

    lines = [self.parse(line) for line in puzzle_input.lines]
    start = time.time()
    try:
      observed = self.solve(lines)
    except Exception:
      observed = format_exc()
    end = time.time()

    return Result(
      elapsed=Duration(start, end),
      expected=puzzle_input.solution,
      input_name=puzzle_input.path.name,
      observed=observed,
    )
