from collections import namedtuple

import sys


class standard():
  초성들 = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
  중성들 = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
  종성들 = [" ", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ",
         "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

  이중모음 = ["ㅑ", "ㅒ", "ㅕ", "ㅖ", "ㅘ", "ㅙ", "ㅛ", "ㅝ", "ㅞ", "ㅠ", "ㅢ"]
  자음 = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
  무성음 = ["ㄱ", "ㄲ", "ㄷ", "ㄸ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
  유성음 = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ", "ㄴ",
         "ㄹ", "ㅇ", "ㅁ"]

  def __init__(self):
    self.letters = []
    self.pronunciation = []

  def run(self, input):
    for c in input:
      self.divide(c)
    return self.pronunciation

  def divide(self, input):
    self.letters = []
    for c in input:
      letter = namedtuple('Coordinate', ['초성', '중성', '종성'])
      if ord('가') <= ord(c) <= ord('힣'):
        한글번호 = ord(c) - ord("가")
        종성번호 = int(한글번호 % 28)
        중성번호 = int(((한글번호 - 종성번호) / 28) % 21)
        초성번호 = int((((한글번호 - 종성번호) / 28) / 21))

        letter.종성 = self.종성들[종성번호]
        letter.중성 = self.중성들[중성번호]
        letter.초성 = self.초성들[초성번호]

        self.letters.append(letter)

  def getLetters(self):
    return self.letters

  def getPronunciation(self):
    temp = []
    for letter in self.letters:
      if letter.초성 in self.자음:
        temp.append(letter.초성)
      if letter.중성 in self.중성들:
        temp.append(letter.중성)
      if letter.종성 in self.초성들:
        temp.append(letter.종성)

    if temp[0] in self.유성음:
      temp.insert(0, 'S')

    if temp[-1] in self.유성음:
      temp.append('S')

    return temp

  def PhonemeToString(self, phonemes):
    '''
    temp = []
    temp.append(phonemes[0])
    for i in range(1, len(phonemes)):
      if phonemes[i] != phonemes[i-1]:
        temp.append(phonemes[i])
    '''
    temp = phonemes
    
    ret = ""
    for i in range(len(temp)):
      ret += temp[i]
    
    return ret

if __name__=='StandardPro':
  std = standard()
  print(std.PhonemeToString(sys.argv[1]))