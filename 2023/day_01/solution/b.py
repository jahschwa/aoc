#          | Day01b   | Day01b_jfred | Day01b_jfred_list
# ---------+----------+--------------+------------------
#   10.txt | 0.005259 |   0.037673   | 0.015199
#  100.txt | 0.008386 |   2.032034   | 0.147402
# 1000.txt | 0.018800 | 180.659451   | 1.354501


from collections import defaultdict
import re

from a import Day01a


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


class Day01b_jfred(Day01b):

  def __init__(self):

    self.words = {word: str(idx + 1) for (idx, word) in enumerate(self.WORDS)}
    self.regex = re.compile('|'.join(self.words))
    self.shortest = len(min(self.words))

  def decode(self, line):

    line = self.replace_words(line)
    return super().decode(line)

  def first_num(self, line, reverse=False):

    return super(Day01b, self).first_num(line, reverse)

  def replace_words(self, line):

    idx = 0
    while True:
      match = self.regex.search(line, idx)
      if not match:
        break
      word = match.group()
      line = (
        line[: match.start()]
        + self.words[word]
        + word[-1]
        + line[match.end() :]
      )

    return line


class Day01b_jfred_list(Day01b_jfred):

  def replace_words(self, line):

    result = []
    idx = 0
    while True:
      match = self.regex.search(line, idx)
      if not match:
        break
      (word, end) = (match.group(), match.end())
      result += [
        line[idx : match.start()],
        self.words[word],
      ]
      idx = end - 1

    result.append(line[idx :])

    return ''.join(result)
