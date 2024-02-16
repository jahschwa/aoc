#!/usr/bin/env python3

from contextlib import nullcontext
from dataclasses import dataclass, fields
from pathlib import Path
import sys


@dataclass
class PuzzleInput:
  path: Path
  solution: int
  lines: list[str]
  base: Path = None

  SEP = '#'

  @classmethod
  def parse(
    cls: type['PuzzleInput'], path: Path | str, seen: list[Path] = None
  ) -> 'PuzzleInput':

    def fatal(exc: Exception):
      print(
        '\n'.join(
          ['PuzzleInput stack:']
          + [f'  {path}' for path in seen]
          + ['']
        ),
        file=sys.stderr,
      )
      raise exc

    path = Path(path).resolve()
    seen = seen or []
    seen.append(path)
    if path in seen[:-1]:
      fatal(RuntimeError('PuzzleInput import cycle'))

    (meta, text, in_text) = ([], [], False)
    try:
      with open(path) as file:
        for line in file:
          if (line := line.strip()).startswith(cls.SEP):
            in_text = True
          else:
            (text if in_text else meta).append(line)
    except Exception as e:
      fatal(e)

    metadata = {}
    data_fields = {field.name: field for field in fields(cls)}
    for line in meta:
      if not line:
        continue
      (key, val) = map(str.strip, line.split('=', 1))
      metadata[key] = data_fields[key].type(val)

    if base := metadata.get('base'):
      metadata['base'] = base if base.is_absolute() else path.parent / base
      text = cls.parse(metadata['base'], seen).lines

    while not text[-1]:
      del text[-1]

    return cls(path=path, lines=text, **metadata)
