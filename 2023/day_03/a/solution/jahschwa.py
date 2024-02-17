from dataclasses import dataclass, field

from base import Solution


class Day03a(Solution):

  def solve(self, lines):

    return sum(part.number for part in Schematic.parse(lines))


@dataclass
class Part:

  row: int
  start_col: int
  end_col: int
  number: int


class Schematic:

  IGNORE = '.'

  def __init__(self, parts, symbols):

    self.parts = parts
    self.symbols = symbols

  @classmethod
  def parse(cls, lines):

    parts = []
    symbols = {}

    def add_part(row, end_col, num):
      parts.append(
        Part(row, end_col - len(num) + 1, end_col, int(num))
      )

    for (row, line) in enumerate(lines):
      current = []
      for (col, c) in enumerate(line):
        if c.isdigit():
          current.append(c)
          continue
        if c not in Schematic.IGNORE:
          symbols[(row, col)] = Symbol(row, col, c)
        if current:
          add_part(row, col - 1, ''.join(current))
          current = []
      if current:
        add_part(row, col - 1, ''.join(current))

    return cls(parts, symbols)

  def adjacent_symbols(self, part, limit=None, allow=None):

    symbols = {}
    (left, right) = (part.start_col - 1, part.end_col + 1)

    def add_symbol(row, col):
      if (
        (symbol := self.symbols.get((row, col)))
        and (not allow or symbol.char in allow)
      ):
          symbols[(row, col)] = symbol

    for row in (part.row - 1, part.row + 1):
      for col in range(left, right + 1):
          add_symbol(row, col)
          if limit and len(symbols) >= limit:
            return symbols

    row = part.row
    for col in (left, right):
      add_symbol(row, col)
      if limit and len(symbols) >= limit:
        return symbols

    return symbols

  def __iter__(self):

    for part in self.parts:
      if self.adjacent_symbols(part, 1):
        yield part


@dataclass(frozen=True)
class Symbol:
  row: int
  col: int
  char: str = field(compare=False)
