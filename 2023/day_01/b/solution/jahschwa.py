#          | Day01b   | Day01b_jfred | Day01b_jfred_list
# ---------+----------+--------------+------------------
#   10.txt | 0.005259 |   0.037673   | 0.015199
#  100.txt | 0.008386 |   2.032034   | 0.147402
# 1000.txt | 0.018800 | 180.659451   | 1.354501


from collections import defaultdict

from a.solution.jahschwa import Day01a


class Day01b(Day01a):

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
