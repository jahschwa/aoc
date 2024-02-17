#!/usr/bin/env python3

from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from importlib import util as imp
from inspect import getmembers, isclass
from pathlib import Path
from pprint import pprint
import sys
import time

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from base import GREEN, RED, RESET, YELLOW, Result, Solution
from puzzle_input import PuzzleInput


def main(
  puzzle_dir: Path,
  class_prefix: str,
  input_file: Path | None = None,
  quiet: bool = False,
  skip: list = None,
  verbose: int = 0,
):

  runner = PuzzleRunner(
    class_prefix=class_prefix,
    puzzle_dir=puzzle_dir,
    extra_input=input_file,
    skip=skip,
  )
  if verbose >= 2:
    pprint(runner)
    print()

  runner.run(pre_output=(verbose >= 1))


@dataclass
class PuzzleRunner:

  class_prefix: str
  puzzle_dir: Path

  extra_input: Path | None = None
  skip: set | None = None

  _input_dir: Path = None
  _solution_dir: Path = None

  _inputs: list[PuzzleInput] | None = None
  _results: dict[str, list[Result]] | None = None
  _solutions: dict[str, list[Solution]] | None = None

  INPUT_DIR_NAME = 'input'
  SOLUTION_DIR_NAME = 'solution'

  def __post_init__(self):

    self.skip = set(self.skip or [])

    self._input_dir = self.puzzle_dir / self.INPUT_DIR_NAME
    self._solution_dir = self.puzzle_dir / self.SOLUTION_DIR_NAME

  def prepare(self, output=False):

    sys.path.insert(0, str(self.puzzle_dir.parent))

    self._inputs = self._gather_inputs()
    self._solutions = self._gather_solutions()

    if output:
      print(self)

  def run(self, output=True, pre_output=False):

    if self._results is None:

      if self._inputs is None:
        self.prepare(pre_output)

      self._results = {}
      for (file_name, solutions) in self._solutions.items():
        for solution in solutions:
          key = f'{file_name}.{type(solution).__name__}'
          self._results[key] = input_results = []
          for puzzle_input in self._inputs:
            input_results.append(solution._solve(puzzle_input))
          if output:
            print(self._to_str_solution(key, input_results), flush=True)

  def _gather_inputs(self) -> list[PuzzleInput]:

    inputs = [
      PuzzleInput.parse(path)
      for path in sorted(self._input_dir.iterdir())
      if path.is_file() and path.name not in self.skip
    ]

    if self.extra_input:
      if not self.extra_input.is_file():
        raise RuntimeError(f'not a file: {self.extra_input}')
      inputs.append(PuzzleInput.parse(self.extra_input))

    return inputs

  def _gather_solutions(self) -> dict[str, list[Solution]]:

    solutions = {}

    for solution_file in self._solution_dir.iterdir():
      if not solution_file.is_file() or solution_file.suffix != '.py':
        continue
      spec = imp.spec_from_file_location(solution_file.stem, solution_file)
      mod = imp.module_from_spec(spec)
      spec.loader.exec_module(mod)
      solutions[solution_file.stem] = [
        obj() for (name, obj) in getmembers(mod, isclass)
        if name.startswith(self.class_prefix)
      ]

    return solutions

  def _to_str_init(self):

    return super().__str__()

  def _to_str_post(self):

    lines = []
    for (name, results) in self._results.items():
      lines += self._to_str_solution(name, results)

    return '\n'.join(lines)

  def _to_str_pre(self):

    lines = ['========== inputs ==========']
    lines += [puzzle_input.path.name for puzzle_input in self._inputs]

    lines += ['========== solutions ==========']
    for (name, solutions) in self._solutions.items():
      lines += [name]
      lines += [f'    {type(solution).__name__}' for solution in solutions]

    lines += ['']
    return '\n'.join(lines)

  def _to_str_solution(self, name, results):

    lines = [f'========== {name} ==========']
    rows = []
    longest = [0, 0]

    for result in results:
      row = [result.input_name, result.elapsed]
      if isinstance(result.observed, str):
        row += [RED, 'ERROR', 50 * '-', result.observed, 50 * '-', RESET]
      else:
        row += [
          GREEN if result.correct else RED,
          '{} {} {}'.format(
            result.observed,
            '==' if result.correct else '!=',
            result.expected,
          ),
          RESET,
        ]

      rows.append(row)
      longest = [
        max(longest, len(text))
        for (longest, text) in zip(longest, (row[0], row[3]))
      ]

    longest = tuple(longest)
    fmt_prefix = '{:>%d} | {} | '
    fmt = (fmt_prefix + '{}{:^%d}{}') % longest
    err_fmt = (fmt_prefix + '{}{}\n{}\n{}\n{}{}') % (longest[0], )
    lines += [(fmt if len(row) == 5 else err_fmt).format(*row) for row in rows]
    lines.append('')

    return '\n'.join(lines)

  def __str__(self):

    if self._results is None:
      if self._inputs is None:
        return self._to_str_init()
      return self._to_str_pre()
    return self._to_str_post()


def puzzle_id(s):

  s = s.lower()

  year = None
  if '/' in s:
    (year, s) = s.split('/')

  if len(s) < 2 or len(s) > 3:
    raise ValueError('puzzle id must be 2-3 characters')

  (num, which) = (s[:-1], s[-1])
  if s[-1] not in 'ab':
    raise ValueError('puzzle id must end with "a" or "b"')

  return (year, int(num), which)


def warning(msg):

  print(f'{YELLOW}WARNING: {msg}{RESET}', file=sys.stderr)


def get_args():

  ap = ArgumentParser()
  add = ap.add_argument

  add('puzzle', type=puzzle_id, help='[YEAR/]NUM{a,b} e.g. 1a, 2023/2b')

  add(
    '-i', '--input-file', type=Path,
    help='run the solutions against an additional input file',
  )
  add(
    '-q', '--quiet', action='store_true',
    help='suppress warnings',
  )
  add(
    '-s', '--skip', action='append',
    help='skip file names (one name per -s)',
  )
  add(
    '-v', '--verbose', action='count', default=0,
    help='specify multiple times to increase verbosity',
  )

  args = ap.parse_args()

  (year, num, which) = args.puzzle
  del args.puzzle

  if not year:
    year = YEARS[-1]
    if not args.quiet and (datetime.now().year - int(year)) >= 2:
      warning(f'no year specified; using {year}\n')
  year_dir = BASE_DIR / str(year)

  if not year_dir.is_dir():
    ap.error(f'no such year {year}; choices:\n    {", ".join(YEARS)}')

  args.puzzle_dir = year_dir / f'day_{num:02d}' / which
  if (
    not args.puzzle_dir.is_dir()
    or not len(list(args.puzzle_dir.iterdir()))
  ):
    solutions = sorted(
      day.name.split('_', 1)[-1].strip('0') + which.stem
      for day in year_dir.iterdir()
      if day.name.startswith('day_')
      for which in day.iterdir()
      if which.is_dir() and len(list(which.iterdir()))
    )
    ap.error('no such puzzle {}{}; choices for {}:\n    {}'.format(
      num, which, year, ', '.join(solutions)
    ))

  args.class_prefix = f'Day{num:02d}{which}'

  return args


YEARS = sorted(
  path.name
  for path in BASE_DIR.iterdir()
  if len(path.name) == 4 and path.name.startswith('2') and path.name.isdigit()
)


if __name__ == '__main__':
  main(**vars(get_args()))
