#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime
from importlib import util as imp
from inspect import getmembers, isclass
from pathlib import Path
import sys
import time
from traceback import print_exc

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from base import Solution


def main(
  year,
  num,
  which,
  solution_file,
  input_file=None,
  test_input_file=None,
):

  sys.path.insert(0, str(solution_file.parent))

  spec = imp.spec_from_file_location(solution_file.stem, solution_file)
  mod = imp.module_from_spec(spec)
  spec.loader.exec_module(mod)

  cases = []

  if test_input_file and test_input_file.is_file():
    with open(test_input_file) as f:
      test_lines = [line.strip() for line in f]
    cases.append(
      ('test', test_lines[1:], test_lines[0], str)
    )

  if input_file and input_file.is_file():
    with open(input_file) as f:
      puzzle_lines = [line.strip() for line in f]
    cases.append((
      'puzzle',
      puzzle_lines,
      lambda solution: getattr(solution, 'SOLUTION', None),
      None,
    ))

  solutions = [
    obj() for (name, obj) in getmembers(mod, isclass)
    if name.startswith(f'Day{num:02d}{which}')
  ]

  for solution in solutions:
    print(f'========== {type(solution).__name__} ==========')

    for (name, lines, expected, fmt) in cases:
      print(f'----- {name} -----')
      lines = [solution.parse(line) for line in lines]
      start = time.time()
      try:
        observed = solution.solve(lines)
      except Exception:
        print_exc()
        continue
      end = time.time()

      if callable(expected):
        expected = expected(solution)
      print(f'Elapsed  : {end - start :.6f} sec')
      if expected:
        print(f'Expected : {expected}')
      print(f'Observed : {observed}')
      if expected:
        if fmt:
          observed = fmt(observed)
        correct = observed == expected
        print(
          'Correct  : {}{}{}'.format(
            GREEN if correct else RED,
            correct,
            RESET,
          )
        )

    print()


def puzzle_id(s):

  s = s.lower()

  year = datetime.now().year
  if '/' in s:
    (year, s) = s.split('/')

  if len(s) < 2 or len(s) > 3:
    raise ValueError('puzzle id must be 2-3 characters')

  (num, which) = (s[:-1], s[-1])
  if s[-1] not in 'ab':
    raise ValueError('puzzle id must end with "a" or "b"')

  return (year, int(num), which)


def get_args():

  ap = ArgumentParser()
  add = ap.add_argument

  add('puzzle', type=puzzle_id, help='[YEAR/]NUM{a,b} e.g. 1a, 2023/2b')

  add('-i', '--input-file', type=Path)

  args = ap.parse_args()

  (args.year, args.num, args.which) = args.puzzle
  del args.puzzle

  year_dir = BASE_DIR / str(args.year)
  if not year_dir.is_dir():
    ap.error(f'no such year {args.year}; choices: {", ".join(YEARS)}')

  puzzle = f'{args.num:02d}{args.which}'

  solution_dir = year_dir / 'solution'
  args.solution_file = solution_dir / f'day_{puzzle}.py'
  if not args.solution_file.is_file():
    solutions = sorted(
      path.stem.split('_')[-1].strip('0')
      for path in solution_dir.iterdir()
      if path.suffix == '.py'
    )
    ap.error(f'no such puzzle {puzzle}; choices: {", ".join(solutions)}')

  if not args.input_file:
    args.input_file = year_dir / 'input' / f'{args.num:02d}.txt'
  args.test_input_file = year_dir / 'test_input' / f'{puzzle}.txt'

  return args


RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

YEARS = sorted(
  path.name
  for path in BASE_DIR.iterdir()
  if len(path.name) == 4 and path.name.startswith('2') and path.name.isdigit()
)


if __name__ == '__main__':
  main(**vars(get_args()))
