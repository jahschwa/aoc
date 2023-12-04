from collections import defaultdict

from day_01a import Day01a


class Day01b(Day01a):

  SOLUTION = 54078

  WORDS = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
  ]

  def __init__(self):

    self.words = defaultdict(lambda: {})
    for (idx, word) in enumerate(self.WORDS):
      self.words[len(word)][word] = str(idx + 1)

  def first_num(self, line, reverse=False):

    if reverse:
      line = line[::-1]

    for (idx, char) in enumerate(line):
      if char.isdigit():
        return char
      for (length, words) in self.words.items():
        sub = line[idx : idx + length]
        if reverse:
          sub = sub[::-1]
        if (num := words.get(sub)):
          return num

    raise RuntimeError('no number found in "{}"'.format(''.join(line)))
