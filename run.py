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
from puzzle_input import PuzzleInput


FILE_INPUT_EXAMPLE = 'example_{}.txt'
FILE_INPUT_FINAL = 'final_{}.txt'


def main(
  year,
  num,
  which,
  solution_file,
  input_file=None,
  input_name=None,
  example_file=None,
):

  sys.path.insert(0, str(solution_file.parent))

  spec = imp.spec_from_file_location(solution_file.stem, solution_file)
  mod = imp.module_from_spec(spec)
  spec.loader.exec_module(mod)

  cases = {}

  if example_file and example_file.is_file():
    cases['example'] = PuzzleInput.parse(example_file)

  if input_file and input_file.is_file():
    cases[input_name] = PuzzleInput.parse(input_file)

  solutions = [
    obj() for (name, obj) in getmembers(mod, isclass)
    if name.startswith(f'Day{num:02d}{which}')
  ]

  for solution in solutions:
    print(f'========== {type(solution).__name__} ==========')

    for (name, puzzle_input) in cases.items():
      print(f'----- {name} -----')
      lines = [solution.parse(line) for line in puzzle_input.lines]
      start = time.time()
      try:
        observed = solution.solve(lines)
      except Exception:
        print_exc()
        continue
      end = time.time()

      expected = puzzle_input.solution
      print(f'Elapsed  : {end - start :.6f} sec')
      print(f'Expected : {expected}')
      print(f'Observed : {observed}')
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
  add('-I', '--input-name', default='final')

  args = ap.parse_args()

  (args.year, args.num, args.which) = args.puzzle
  del args.puzzle

  year_dir = BASE_DIR / str(args.year)
  if not year_dir.is_dir():
    ap.error(f'no such year {args.year}; choices:\n    {", ".join(YEARS)}')

  puzzle_dir = year_dir / f'day_{args.num:02d}'
  args.solution_file = puzzle_dir / f'solution/{args.which}.py'
  if not args.solution_file.is_file():
    solutions = sorted(
      day.name.split('_', 1)[-1].strip('0') + solution.stem
      for day in year_dir.iterdir()
      if day.name.startswith('day_')
      for solution in (day / 'solution').iterdir()
      if solution.is_file()
    )
    ap.error('no such puzzle {}{}; choices for {}:\n    {}'.format(
      args.num, args.which, args.year, ', '.join(solutions)
    ))

  input_dir = puzzle_dir / 'input'

  if not args.input_file:
    args.input_file = input_dir / FILE_INPUT_FINAL.format(args.which)

  args.example_file = input_dir / FILE_INPUT_EXAMPLE.format(args.which)

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
