import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView
from keras.models import load_model
import threading
import time
from source import Statistics

uipath = os.path.abspath(os.path.dirname(__file__)) + '/UI resource/MAIN_UI.ui'
form_class = uic.loadUiType(uipath)[0]

class MainWindow(QMainWindow, form_class):

  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.testbutton.clicked.connect(self.testbtn_clicked)
    self.trainbutton.clicked.connect(self.trainbtn_clicked)
    self.statbutton.clicked.connect(self.statbtn_clicked)
    self.exitbutton.clicked.connect(self.exitbtn_clicked)
    self.tableView = QTableView()
    self.tableView.setWindowTitle('Statistics')
    self.testWindow = TestWindow.TestWindow(self)
    self.trainWindow = TrainWindow.TrainWindow(self)


  def testbtn_clicked(self):
    self.testWindow.__init__()
    self.testWindow.show()
    self.destroy()

  def trainbtn_clicked(self):
    self.testWindow.__init__()
    self.trainWindow.show()
    self.destroy()
  def statbtn_clicked(self):
    self.__make_table()
  def exitbtn_clicked(self):
    sys.exit()

  def __make_table(self):
    LUT = ['ㄱ', 'ㄷ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
      , 'ㅏ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅐ', 'ㅕ', 'ㅗ', 'ㅘ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅟ', 'ㅠ'
      , 'ㅡ', 'ㅣ', 'ㄴ', 'ㄹ', 'ㅇ', 'ㅁ', 'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ']
    data = Statistics.buildCSV()
    self.model = QStandardItemModel(34, 6, self)
    names = ["Phoneme", "HitRate", "NumOfQuiz", "NumOfRight", "NumOfWrong", "AverageAccuracy"]
    ret = []
    for i in range(0, 34):
      temp = []
      temp.append(LUT[i])
      ret.append(temp + data[i])

    self.model.setHorizontalHeaderLabels(names)

    for i in range(0, len(ret)):
      for j in range(0, len(ret[0])):
        self.item = QStandardItem(ret[i][j])
        self.model.setItem(i, j, self.item)
    self.tableView.resize(750,450)
    self.tableView.setModel(self.model)
    self.tableView.show()
  def closeEvent(self,event):
    sys.exit()

models = []
if __name__=='MainWindow':
  models.append(load_model('./resource/Models/tot_u.hdf5'))
  print("Learned Model Loading |**          |")
  models.append(load_model('./resource/Models/tot_v.hdf5'))
  print("Learned Model Loading |****        |")
  models.append(load_model('./resource/Models/YGD.hdf5'))
  print("Learned Model Loading |******      |")
  models.append(load_model('./resource/Models/PMP.hdf5'))
  print("Learned Model Loading |********    |")
  models.append(load_model('./resource/Models/YCGYH.hdf5'))
  print("Learned Model Loading |**********  |")
  models.append(load_model('./resource/Models/TOT.hdf5'))
  print("Learned Model Loading |************|")

import TestWindow
import TrainWindow