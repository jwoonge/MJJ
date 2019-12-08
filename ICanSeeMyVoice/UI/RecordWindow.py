import sys
import os

from source import Recorder
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView
import threading
import time

uipath = os.path.abspath(os.path.dirname(__file__)) + '/UI resource/RECORD_UI.ui'
form_class4 = uic.loadUiType(uipath)[0]

class RecordWindow(QMainWindow, form_class4):
  def __init__(self,parent = None):
    super(RecordWindow, self).__init__(parent)
    self.setupUi(self)
    self.record_button.clicked.connect(self.record_btn_clicked)
    self.record_btn_signal = True

    #self.sema = threading.Thread(target=self.t.RECORDERfunc)

    self.sema2 = threading.Thread(target=self.printtime)
    self.sema2.setDaemon(True)
    self.time = 0
    self.timevar = QTimer()
    self.timevar.setInterval(100)
    self.timevar.timeout.connect(self.printtime)
  def record_btn_clicked(self):

    if self.record_btn_signal == True:
      self.record_button.setText('Stop Recording')
      self.record_btn_signal = False
      self.record_button.repaint()
      #self.t.init()
      self.t = Recorder.recorder()
      self.timevar.start()
      self.sema = threading.Thread(target=self.t.RECORDERfunc)
      self.sema.setDaemon(True)
      self.sema.start()
      self.record_button.repaint()

    elif (self.record_btn_signal == False):
      self.t.recsignal = False
      self.record_button.setText('Recording')
      self.record_button.repaint()
      self.record_btn_signal = True
      self.destroy()
  def printtime(self):
    if self.time < 1 :
      self.record_button.setEnabled(False)

    else :
      self.record_button.setEnabled(True)
    self.time += 0.1
    self.textBrowser.setText('%s' %round(self.time,2))
    self.textBrowser.repaint()
    if(self.time == 5) :
      self.t.recsignal = False
    if(self.time >5.2) :
      self.destroy()
  def closeEvent(self,event):
    self.t.recsignal = False
    self.destroy()