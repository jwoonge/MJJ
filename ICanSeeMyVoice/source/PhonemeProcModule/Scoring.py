from keras.models import load_model
from collections import namedtuple
from HangulTable import *
import numpy as np

def Calc_class(model, mfcc, indextoAdv, valueAdv, confidence=False):
  confidences_np = (model.predict(mfcc, verbose=0)).reshape(-1)
  confidences = []
  for i in range(len(confidences_np)):
    confidences.append(confidences_np[i].astype(np.float64))

  for i in range(len(indextoAdv)):
    confidences[indextoAdv[i]] *= (100+valueAdv)/100

  if confidence :
    return confidences
  
  else :
    maxValue = confidences[0]
    maxIndex = 0
    for i in range(len(confidences)):
      if maxValue < confidences[i]:
        maxIndex = i
        maxValue = confidences[i]
    return maxIndex

def int_phonemes(Pronun):
  int_pronun = []
  for i in range(len(Pronun)):
    if Pronun[i] == 'ㅒ':
      int_pronun.append('ㅖ')
    elif Pronun[i] == 'ㅞ' or Pronun[i] == 'ㅙ':
      int_pronun.append('ㅚ')
    elif Pronun[i] == 'ㅢ':
      int_pronun.append('ㅡ')
    elif Pronun[i] == 'ㅐ':
      int_pronun.append('ㅔ')
    else:
      int_pronun.append(Pronun[i])
  return int_pronun


def pickBestN(input_list, N, xy='x'):
  temp = []
  for i in range(len(input_list)):
    t = namedtuple("Coordinate", ['value', 'index'])
    t.value = input_list[i]
    t.index = i
    temp.append(t)
  temp = sorted(temp, key=lambda x: x.value, reverse=True)
  ret = []
  if N <= len(temp):
    if xy == 'x':
      for i in range(N):
        ret.append(LUT_vt[temp[i].index])
    elif xy == 'y':
      for i in range(N):
        ret.append(temp[i].value)
  return ret


class Scorer():
  def __init__(self, models):
    self.model_u = models[0]
    self.model_v = models[1]
    self.model_ygd = models[2]
    self.model_pmp = models[3]
    self.model_ycgyh = models[4]
    self.model_tot = models[5]

  def Get_Score(self, Pronun, MFCC, input_UVsound):
    self.Settings(Pronun, MFCC, input_UVsound)
    self.Match_Phoneme()
    self.Scoring()

    return self.scores, self.UV_Matched

  def Get_STT(self, allMFCC):
    self.allMFCC = allMFCC
    return self.Guess_Sound()

  def Scoring(self):
    self.scores = []
    for i in range(len(self.Pronun)):
      temp = namedtuple('score',['phoneme','score'])
      temp.phoneme = self.Pronun[i]
      temp.score = 0
      self.scores.append(temp)

    if not self.UV_Matched :
      return
    for i in range(self.N_phoneme_expected):
      tempmfcc = self.MFCC[self.Match_table[i]]
      tempmfcc = np.reshape(np.array(tempmfcc), [1,5,12,1])

      if self.Match_table[i] == -1:
        temp_score = 0
      else:
        if self.input_UVsound[self.Match_table[i]] == 'U':
          ygd_r, pmp_r, ycgyh_r = GetFeat(self.Pronun[i])
          ygd_list = []
          ygd_list.append(ygd_r)
          pmp_list=[]
          pmp_list.append(pmp_r)
          ycgyh_list=[]
          ycgyh_list.append(ycgyh_r)
          ygd = Calc_class(self.model_ygd, tempmfcc, ygd_list, 15)
          pmp = Calc_class(self.model_pmp, tempmfcc ,pmp_list, 15)
          ycgyh = Calc_class(self.model_ycgyh, tempmfcc, ycgyh_list, 15)
          temp_score = 100
          if ygd_r != ygd:
            temp_score -= 25
          if pmp_r != pmp:
            temp_score -= 25
          if ycgyh_r != ycgyh:
            temp_score -= 25

        else :
          r_index = []
          r_index.append(LUT_vt.index(self.Pronun_int[i]))
          confidences = Calc_class(self.model_v, tempmfcc, r_index, 10, confidence=True)
          bests = pickBestN(confidences,10,'x')
          if not self.Pronun_int[i] in bests :
            temp_score = 0
          else:
            rank = bests.index(self.Pronun_int[i])
            if rank<3:
              temp_score = 100
            elif rank<5:
              temp_score = 75
            elif rank<7:
              temp_score = 50
            else:
              temp_score = 25

      self.scores[i].score = temp_score


  def Guess_Sound(self):
    predicted_phonemes = []

    for i in range(len(self.allMFCC)):
      tempmfcc = np.reshape(np.array(self.allMFCC[i]),[1,5,12,1])

      predicted_phonemes.append(LUT_t[Calc_class(self.model_tot, tempmfcc, self.indextoAdv_t,30)])
    return predicted_phonemes

  def Match_Phoneme(self):
    if len(self.UV_sound) == len(self.UV_text): # UV 매칭되는 경우
      self.UV_Matched = True
      for i in range(len(self.UV_sound)):
        if i%2 == 0 : # 무성음 덩어리의 경우
          self.Match_table[self.UV_text[i][0]] = self.UV_sound[i][0]

        else: # 유성음 덩어리의 경우
          if len(self.UV_sound[i]) > len(self.UV_text[i]): # 기대되는 것보다 더 많이 찾음
            self.Match_table[self.UV_text[i][0]] = self.UV_sound[i][0]
            self.Match_table[self.UV_text[i][-1]] = self.UV_sound[i][-1]
            if len(self.UV_text[i])>2:
              self.Match_table[self.UV_text[i][1]] = self.UV_sound[i][int(len(self.UV_sound[i])/2)]
          
          else :
            for j in range(len(self.UV_sound[i])):
              self.Match_table[self.UV_text[i][j]] = self.UV_sound[i][j]

    else: # UV 매칭 실패 시
      self.UV_Matched = False
      if len(self.input_UVsound) < self.N_phoneme_expected:
        for i in range(len(self.input_UVsound)-1):
          self.Match_table[i] = i
      else:
        for i in range(len(self.Match_table)):
          self.Match_table[i] = i

      self.Match_table[self.N_phoneme_expected-1] = len(self.input_UVsound)-1
      if self.N_phoneme_expected > 3:
        self.Match_table[self.N_phoneme_expected-2] = len(self.input_UVsound)-2

  def Settings(self, Pronun, MFCC, input_UVsound):
    self.UV_Matched = False
    self.Pronun = Pronun
    self.indextoAdv_u = []
    self.indextoAdv_v = []
    self.indextoAdv_t = []
    self.Pronun_int = int_phonemes(Pronun)
    self.MFCC = MFCC
    self.input_UVsound = input_UVsound

    self.UV_text_order, self.UV_text = self.Make_UV_text(self.Pronun_int)
    self.UV_sound_order, self.UV_sound = self.Make_UV_sound(input_UVsound)
    self.N_phoneme_expected = len(Pronun)
    self.Match_table = [-1 for x in range(self.N_phoneme_expected)]  # text index to sound index


  def Make_UV_sound(self, input_UVsound):
    order = []
    index = []
    for i in range(len(input_UVsound)):
      if i == 0:
        tempp = []
        tempp.append(i)
        index.append(tempp)
        order.append(input_UVsound[i])
      else:
        if input_UVsound[i] == order[-1][0]:
          index[-1].append(i)
        else:
          tempp = []
          tempp.append(i)
          index.append(tempp)
          order.append(input_UVsound[i])
    return order, index

  def Make_UV_text(self, Pro):
    input_UVtext = []
    for i in range(len(Pro)):
      if Pro[i] in LUT_vt:
        input_UVtext.append('V')
        if not LUT_vt.index(Pro[i]) in self.indextoAdv_v:
          self.indextoAdv_v.append(LUT_vt.index(Pro[i]))
        if not LUT_t.index(Pro[i]) in self.indextoAdv_t:
          self.indextoAdv_t.append(LUT_t.index(Pro[i]))
      elif Pro[i] in (LUT_ut + ['S']):
        input_UVtext.append('U')
        if Pro[i] != 'S':
          if not LUT_ut.index(Pro[i]) in self.indextoAdv_u:
            self.indextoAdv_u.append(LUT_ut.index(Pro[i]))
          if not LUT_t.index(Pro[i]) in self.indextoAdv_t:
            self.indextoAdv_t.append(LUT_t.index(Pro[i]))

    order = []
    index = []
    for i in range(len(input_UVtext)):
      if i == 0:
        tempp = []
        tempp.append(i)
        index.append(tempp)
        order.append(input_UVtext[i])
      else:
        if input_UVtext[i] == order[-1][0]:
          index[-1].append(i)
        else:
          tempp = []
          tempp.append(i)
          index.append(tempp)
          order.append(input_UVtext[i])

    return order, index