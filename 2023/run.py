#!/usr/bin/env python3

from argparse import ArgumentParser
from importlib import util as imp
from inspect import getmembers, isclass
from pathlib import Path
import sys
import time
from traceback import print_exc

from solution.base import Solution


def main(puzzle, input_file=None):

  (num, which) = (int(puzzle[:-1]), puzzle[-1])

  if not input_file:
    input_file = INPUT_DIR / FMT_INPUT.format(num)
  with open(input_file) as f:
    puzzle_lines = [line.strip() for line in f]

  test_input_file = TEST_INPUT_DIR / FMT_TEST_INPUT.format(num, which)
  with open(test_input_file) as f:
    test_lines = [line.strip() for line in f]
  (test_expected, test_lines) = (test_lines[0], test_lines[1:])

  sys.path.insert(0, str(SOLUTION_DIR))

  solution_file = SOLUTION_DIR / FMT_SOLUTION.format(num, which)
  spec = imp.spec_from_file_location(solution_file.stem, solution_file)
  mod = imp.module_from_spec(spec)
  spec.loader.exec_module(mod)

  cls = FMT_CLASS.format(num, which)
  solutions = [
    obj() for (name, obj) in getmembers(mod, isclass)
    if name.startswith(cls)
  ]

  for solution in solutions:
    print(f'========== {type(solution).__name__} ==========')

    puzzle_lines = [solution.parse(line) for line in puzzle_lines]
    test_lines = [solution.parse(line) for line in test_lines]

    cases = [
      ('test', test_lines, test_expected, str),
      ('puzzle', puzzle_lines, getattr(solution, 'SOLUTION', None), None),
    ]
    for (name, lines, expected, fmt) in cases:
      print(f'----- {name} -----')
      start = time.time()
      try:
        observed = solution.solve(lines)
      except Exception:
        print_exc()
        continue
      end = time.time()

      print(f'Elapsed  : {end - start :.6f} sec')
      if fmt:
        observed = fmt(observed)
      if expected:
        print(f'Expected : {expected}')
      print(f'Observed : {observed}')
      if expected:
        correct = observed == expected
        print(f'Correct  : {correct}')

    print()


def puzzle_id(s):

  s = s.lower()

  if len(s) < 2 or len(s) > 3:
    raise ValueError('puzzle id must be 2-3 characters')

  (num, which) = (s[:-1], s[-1])
  if s[-1] not in 'ab':
    raise ValueError('puzzle id must end with "a" or "b"')

  return num.strip('0') + which


def get_args():

  ap = ArgumentParser()
  add = ap.add_argument

  add('puzzle', choices=SOLUTIONS, type=puzzle_id)

  add('-i', '--input-file', type=Path)

  return ap.parse_args()


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / 'input'
SOLUTION_DIR = BASE_DIR / 'solution'
TEST_INPUT_DIR = BASE_DIR / 'test_input'

SOLUTIONS = set(
  path.stem.split('_')[-1].strip('0')
  for path in SOLUTION_DIR.iterdir()
)

FMT_CLASS = 'Day{:02d}{}'
FMT_INPUT = '{:02d}.txt'
FMT_SOLUTION = 'day_{:02d}{}.py'
FMT_TEST_INPUT = '{:02d}{}.txt'


if __name__ == '__main__':
  main(**vars(get_args()))
