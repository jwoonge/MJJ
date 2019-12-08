import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView
from random import *
from source.PhonemeProcModule import PhonemeProc
from source.PhonemeProcModule import Scoring
from source import RWwav
from source import StandardPro
from source import txtReader
import time
from source import Statistics
from collections import namedtuple
from MainWindow import models

uipath = os.path.abspath(os.path.dirname(__file__)) + '/UI resource/TEST_UI.ui'
form_class2 = uic.loadUiType(uipath)[0]
text = txtReader.Readcsv()

class TestWindow(QMainWindow, form_class2):
  def __init__(self, parent=None):
    self.test_result = []
    self.text_attribute = []

    self.count = 0
    self.scorer = Scoring.Scorer(models)
    super(TestWindow, self).__init__(parent)
    self.setupUi(self)
    self.test_record_button.clicked.connect(self.test_record_btn_clicked)
    self.test_next_button.clicked.connect(self.test_next_btn_clicked)
    self.test_exit_button.clicked.connect(self.test_exit_btn_clicked)
    self.test_result_button.clicked.connect(self.test_result_btn_clicked)
    self.TestResult = [0 for x in range(35)]
    self.test_result_button.setEnabled(False)
    self.txtdivide = StandardPro.standard()
    self.record_btn_signal = True
    self.test_next_button.setEnabled(False)
    self.Phonem_counts = [0 for x in range(35)]
    self.LUT = ['ㄱ', 'ㄷ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
      , 'ㅏ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅐ', 'ㅕ', 'ㅗ', 'ㅘ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅟ', 'ㅠ'
      , 'ㅡ', 'ㅣ', 'ㄴ', 'ㄹ', 'ㅇ', 'ㅁ', 'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ']
    self.recordWindow = RecordWindow()
    self.MassageBox = MassageWindow()
    self.PhonemeProc = PhonemeProc.PhonemeProc(16000)

    self.setWord()

  def setWord(self):
    a = randint(1, 3019)
    self.text1 = text.loc[a,0]
    self.text2 = text.loc[a,1]

    self.txtdivide.divide(self.text2)
    self.letters = self.txtdivide.getLetters()

    while(len(self.letters)<3):
      temp = namedtuple('Coordinate',['초성','중성','종성'])
      temp.초성 = ""
      temp.중성 = ""
      temp.종성 = ""
      self.letters.append(temp)
    self.pronun = self.txtdivide.getPronunciation()

    self.textBrowser_set()

    
  def textBrowser_set(self):
    self.text_attribute = []
    self.textBrowser.setText('%s' % self.text1)
    self.textBrowser_2.setText('%s' % self.letters[0].초성)
    self.text_attribute.append(self.letters[0].초성)
    self.textBrowser_3.setText('%s' % self.letters[0].중성)
    self.text_attribute.append(self.letters[0].중성)
    self.textBrowser_4.setText('%s' % self.letters[0].종성)
    self.text_attribute.append(self.letters[0].종성)
    self.textBrowser_5.setText('%s' % self.letters[1].초성)
    self.text_attribute.append(self.letters[1].초성)
    self.textBrowser_6.setText('%s' % self.letters[1].중성)
    self.text_attribute.append(self.letters[1].중성)
    self.textBrowser_7.setText('%s' % self.letters[1].종성)
    self.text_attribute.append(self.letters[1].종성)
    self.textBrowser_8.setText('%s' % self.letters[2].초성)
    self.text_attribute.append(self.letters[2].초성)
    self.textBrowser_9.setText('%s' % self.letters[2].중성)
    self.text_attribute.append(self.letters[2].중성)
    self.textBrowser_10.setText('%s' % self.letters[2].종성)
    self.text_attribute.append(self.letters[2].종성)

  def test_result_btn_clicked(self):

    self.test_result_button.setEnabled(False)

    self.MassageBox.__init__()


    wavpath = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/resource/wav/'
    pcm, s = RWwav.Read_file(wavpath + "testRecorded.wav")
    Normal_value = Normalization(pcm)



    if Normal_value < 2:
      self.MassageBox.textBrowser.setText('마이크와의 거리가 너무 가깝습니다.\n다시 녹음 해 주세요.\nYou are so close to mike\nPlease Try Again!')
      self.MassageBox.show()
      self.test_result_button.setEnabled(False)
    elif Normal_value > 4:
      self.MassageBox.textBrowser.setText('마이크와의 거리가 너무 멉니다.\n다시 녹음 해 주세요.\nYou are so far to mike\nPlease Try Again!')
      self.MassageBox.show()
      self.test_result_button.setEnabled(False)
    else:
      phonemes,uvsound = self.PhonemeProc.getPhonemes(pcm)
      self.scorelist, valid = self.scorer.Get_Score(self.txtdivide.getPronunciation(),phonemes, uvsound)
      self.colloring_word(self.scorelist)
      self.textBrowser_set()
      self.test_next_button.setEnabled(True)
      self.test_record_button.setText('Recording')
      self.test_record_button.setEnabled(False)



  def test_record_btn_clicked(self):
    self.recordWindow.__init__()
    self.test_record_button.setText('Retry')
    self.test_record_button.repaint()
    self.recordWindow.show()
    self.test_result_button.setEnabled(True)
    self.test_result_button.repaint()


  def test_next_btn_clicked(self):
    self.initail_word_collor()
    self.count += 1
    tempstring = '/10'
    tempcount = self.count+1
    count_string = str(tempcount) + tempstring
    self.label.setText(count_string)
    if self.scorelist[0].phoneme == 'S':
      del (self.scorelist[0])
    if self.scorelist[-1].phoneme == 'S':
      del (self.scorelist[-1])

    for i in range(len(self.scorelist)) :
      temp = namedtuple('TESTRESULT', ['phoneme', 'accuracy', 'isCorrect'])
      temp.phoneme = self.scorelist[i].phoneme
      temp.accuracy = self.scorelist[i].score
      if self.scorelist[i].score >= 75 :
        temp.isCorrect = True
      else :
        temp.isCorrect = False
      self.test_result.append(temp)
    for i in range(len(self.test_result)):

      if self.test_result[i].phoneme == 'ㅞ' or self.test_result[i].phoneme == 'ㅙ':
        self.test_result[i].phoneme = 'ㅚ'
      elif self.test_result[i].phoneme == 'ㅔ':
        self.test_result[i].phoneme = 'ㅐ'
      elif self.test_result[i].phoneme == 'ㅖ':
        self.test_result[i].phoneme = 'ㅒ'
      elif self.test_result[i].phoneme == 'ㅢ':
        self.test_result[i].phoneme = 'ㅡ'


    if self.count == 10:
      self.count = 0
      temp = Statistics.buildCSV()
      Statistics.AddToCSV(self.test_result, temp)
      self.Get_Test_result()
      self.label.setText('Test is End')
      self.test_record_button.setEnabled(False)
      self.test_result_button.setEnabled(False)
      self.test_next_button.setEnabled(False)
    else :

      self.test_record_button.setEnabled(True)
      self.test_next_button.setEnabled(False)
      self.test_record_button.repaint()
      self.test_record_button.setText('Recording')
      self.setWord()
      self.repaint()



  def test_exit_btn_clicked(self):
    self.mainWindow2 = MainWindow()
    self.mainWindow2.show()
    self.destroy()
  def initail_word_collor(self):
    colorvar = QColor(0,0,0)
    self.textBrowser_2.setTextColor(colorvar)
    self.textBrowser_3.setTextColor(colorvar)
    self.textBrowser_4.setTextColor(colorvar)
    self.textBrowser_5.setTextColor(colorvar)
    self.textBrowser_6.setTextColor(colorvar)
    self.textBrowser_7.setTextColor(colorvar)
    self.textBrowser_8.setTextColor(colorvar)
    self.textBrowser_9.setTextColor(colorvar)
    self.textBrowser_10.setTextColor(colorvar)

  def colloring_word(self,scores):
    # if score1 <60
    if self.scorelist[0].phoneme == 'S':
      del (self.scorelist[0])
    if self.scorelist[-1].phoneme == 'S':
      del (self.scorelist[-1])
    colorvar_red = QColor(255, 0, 0)  # 빨간색 SCORE[i] < 50
    colorvar_green = QColor(0, 255, 0)  # 녹색 SCORE[i] > 80
    colorvar_orange = QColor(255, 128, 64)  # 주황색[i]  50 <SCORE < 80
    colorvar_black = QColor(0,0,0)
    textbrowsers = [self.textBrowser_2,self.textBrowser_3,self.textBrowser_4,self.textBrowser_5,self.textBrowser_6,self.textBrowser_7,
                    self.textBrowser_8,self.textBrowser_9,self.textBrowser_10]


    temp = 0
    for i in range (len(scores))  :
      if scores[i].score < 20 :
        while temp < 9 :
          if self.text_attribute[temp] == scores[i].phoneme:
            textbrowsers[temp].setTextColor(colorvar_red)
            temp += 1
            break
          temp+=1

      elif scores[i].score < 75 :
        while temp < 9 :
          if self.text_attribute[temp] == scores[i].phoneme:
            textbrowsers[temp].setTextColor(colorvar_orange)
            temp += 1
            break
          temp+=1

      elif scores[i].score >= 75:
        while temp < 9 :
          if self.text_attribute[temp] == scores[i].phoneme:
            textbrowsers[temp].setTextColor(colorvar_green)
            temp += 1
            break
          temp+=1



  def Get_Test_result(self):

    ret = []
    tempstring = 'Test Result\n'

    for i in range(len(self.test_result)) :

      if self.test_result[i].phoneme == 'ㅞ' or self.test_result[i].phoneme =='ㅙ':
        self.test_result[i].phoneme = 'ㅚ'
      elif self.test_result[i].phoneme == 'ㅔ':
        self.test_result[i].phoneme = 'ㅐ'
      elif self.test_result[i].phoneme =='ㅖ':
        self.test_result[i].phoneme = 'ㅒ'
      elif self.test_result[i].phoneme == 'ㅢ' :
        self.test_result[i].phoneme = 'ㅡ'

      index = self.LUT.index(self.test_result[i].phoneme)
      self.TestResult[index] += int(self.test_result[i].accuracy)
      self.Phonem_counts[index] += 1


    for i in range(len(self.TestResult)) :
        ret_tuple = namedtuple('Test_Result',['phoneme', 'count', 'score'])
        ret_tuple.phoneme = i
        ret_tuple.count = self.Phonem_counts[i]
        ret_tuple.score = self.TestResult[i]
        ret.append(ret_tuple)
    for i in range(len(ret)) :
      if ret[i].count != 0 :
         tempstring +=  (self.LUT[i]+'->' + 'counts :')
         tempstring +=  (format(self.Phonem_counts[i],".2f") + '   average :')
         tempstring += (format((self.TestResult[i]/self.Phonem_counts[i]),".2f") + '\n')
    self.MassageBox.textBrowser.setText(tempstring)
    self.MassageBox.show()

  def closeEvent(self,event):
    if self.MassageBox :
      self.MassageBox.destroy()
    if self.recordWindow :
      self.recordWindow.destroy()
    self.mainWindow2 = MainWindow()
    self.mainWindow2.show()
    self.destroy()



def Normalization(pcmValue):
  pcm_max = max(pcmValue)
  pcm_min = abs(min(pcmValue))
  if pcm_max < pcm_min:
    pcm_max = pcm_min
  del pcm_min
  Normalization_rate = 10000 / pcm_max
  print('Normalization rate : ', Normalization_rate)
  for i in range(len(pcmValue)):
    pcmValue[i] = int(float(pcmValue[i]) * Normalization_rate)
  return Normalization_rate
from RecordWindow import RecordWindow
from MainWindow import MainWindow
from MassageWindow import MassageWindow