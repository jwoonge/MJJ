import os
from source import Recorder
from source import RWwav
from source import txtReader
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView
from random import *
from source.PhonemeProcModule import PhonemeProc
from source.PhonemeProcModule import Scoring
from source import StandardPro
import time
from collections import namedtuple
from MainWindow import models

uipath = os.path.abspath(os.path.dirname(__file__)) + '/UI resource/TRAIN_UI.ui'
form_class1 = uic.loadUiType(uipath)[0]
text = txtReader.Readcsv()


class TrainWindow(QMainWindow, form_class1):
  def __init__(self, parent=None):
    super(TrainWindow, self).__init__(parent)
    self.text_attribute = []
    self.setupUi(self)
    self.train_record_button.clicked.connect(self.train_record_btn_clicked)
    self.train_next_button.clicked.connect(self.train_next_btn_clicked)
    self.train_exit_button.clicked.connect(self.train_exit_btn_clicked)
    self.train_result_button.clicked.connect(self.train_result_btn_clicked)

    self.scorer = Scoring.Scorer(models)
    self.PhonemeProc = PhonemeProc.PhonemeProc(16000)
    self.train_result_button.setEnabled(False)
    self.record_btn_signal = True
    self.txtdivide = StandardPro.standard()
    self.train_next_button.setEnabled(False)
    self.MassageBox = MassageWindow()
    self.recordWindow = RecordWindow()
    self.setWord()

  def setWord(self):
    a = randint(1, 3019)
    self.text1 = text.loc[a, 0]
    self.text2 = text.loc[a, 1]

    self.txtdivide.divide(self.text2)
    self.letters = self.txtdivide.getLetters()

    while (len(self.letters) < 3):
      temp = namedtuple('Coordinate', ['초성', '중성', '종성'])
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
    self.textBrowser_11.setText('')
  def train_result_btn_clicked(self):
    self.train_result_button.setEnabled(False)
    self.MassageBox.__init__()

    wavpath = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/resource/wav/'
    pcm, s = RWwav.Read_file(wavpath + "testRecorded.wav")
    Normal_value = Normalization(pcm)

    if Normal_value < 2 :
      self.MassageBox.textBrowser.setText('마이크와의 거리가 너무 가깝습니다.\n다시 녹음 해 주세요.\nYou are so close to mike\nPlease Try Again!')
      self.MassageBox.show()
      self.train_result_button.setEnabled(False)
    elif Normal_value > 4 :
      self.MassageBox.textBrowser.setText('마이크와의 거리가 너무 멉니다.\n다시 녹음 해 주세요.\nYou are so far to mike\nPlease Try Again!')
      self.MassageBox.show()
      self.train_result_button.setEnabled(False)
    else :
      phonemes, uvsound = self.PhonemeProc.getPhonemes(pcm)
      self.scorelist, valid = self.scorer.Get_Score(self.txtdivide.getPronunciation(), phonemes, uvsound)
      if not valid :
        self.MassageBox.textBrowser.setText('ICANSEEMYVOICE가 적절한 음성을 찾지 못했습니다.\n다시 녹음 할 수 있습니다..\nICANSEEMYVOICE can not found a valid sounds.\nYou Can Try Again!')
        self.MassageBox.show()
      else :
        self.train_record_button.setText('Recording')
      
      self.expectlist = self.scorer.Get_STT()
      if self.expectlist[0] == 'S':
        del (self.expectlist[0])
      if self.expectlist[-1] == 'S':
        del (self.expectlist[-1])

      expect = self.txtdivide.PhonemeToString(self.expectlist)
      self.colloring_word(self.scorelist)
      self.textBrowser_set()
      self.textBrowser_11.setText(expect)
      self.train_next_button.setEnabled(True)


  def colloring_word(self,scores):
    # if score1 <60
    if self.scorelist[0].phoneme == 'S':
      del (self.scorelist[0])
    if self.scorelist[-1].phoneme == 'S':
      del (self.scorelist[-1])
    colorvar_red = QColor(255, 0, 0)  # 빨간색 SCORE[i] < 50
    colorvar_green = QColor(0, 255, 0)  # 녹색 SCORE[i] > 80
    colorvar_orange = QColor(255, 128, 64)  # 주황색[i]  50 <SCORE < 80
    colorvar_black = QColor(0, 0, 0)
    textbrowsers = [self.textBrowser_2, self.textBrowser_3, self.textBrowser_4, self.textBrowser_5, self.textBrowser_6,
                    self.textBrowser_7,
                    self.textBrowser_8, self.textBrowser_9, self.textBrowser_10]

    temp = 0
    for i in range(len(scores)):
      if scores[i].score < 20:
        while temp < 9:
          if self.text_attribute[temp] == scores[i].phoneme:
            textbrowsers[temp].setTextColor(colorvar_red)
            temp += 1
            break
          temp += 1

      elif scores[i].score < 75:
        while temp < 9:
          if self.text_attribute[temp] == scores[i].phoneme:
            textbrowsers[temp].setTextColor(colorvar_orange)
            temp += 1
            break
          temp += 1

      elif scores[i].score >= 75:
        while temp < 9:
          if self.text_attribute[temp] == scores[i].phoneme:
            textbrowsers[temp].setTextColor(colorvar_green)
            temp += 1
            break
          temp += 1
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

  def train_record_btn_clicked(self):
    self.train_record_button.setText('Retry')
    self.train_record_button.repaint()
    self.recordWindow.__init__()
    self.recordWindow.show()
    self.train_result_button.setEnabled(True)
    self.train_result_button.repaint()

  def train_next_btn_clicked(self):
    self.initail_word_collor()
    self.train_record_button.setEnabled(True)
    self.train_next_button.setEnabled(False)
    self.train_record_button.setText('Recording')
    self.train_record_button.repaint()
    self.setWord()

  def train_exit_btn_clicked(self):
    self.mainWindow = MainWindow()
    self.mainWindow.show()
    self.destroy()
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
    if pcm_max < pcm_min :
        pcm_max = pcm_min
    del pcm_min
    Normalization_rate = 10000 / pcm_max
    print('Normalization rate : ',Normalization_rate)
    for i in range(len(pcmValue)):
      pcmValue[i] = int(float(pcmValue[i]) * Normalization_rate)
    return Normalization_rate

from RecordWindow import RecordWindow
from MainWindow import MainWindow
from MassageWindow import MassageWindow
