import sys
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/pi/Desktop/ICanSeeMyVoice/ICSV pkg')
sys.path.append('C:\\Users\\JooHwan\\PycharmProjects\\ICANSEEMYVOICE\\venv\\ICSV pkg')
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import *
import StandardPro
import Recorder
import txtReader
import threading
import time

form_class = uic.loadUiType("UI source/MAIN UI.ui")[0]
form_class1 = uic.loadUiType("UI source/TRAIN UI.ui")[0]
form_class2 = uic.loadUiType("UI source/TEST UI.ui")[0]
form_class3 = uic.loadUiType("UI source/STAT UI.ui")[0]
form_class4 = uic.loadUiType("UI source/RECORD UI.ui")[0]
text = txtReader.Readcsv()



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

    if (self.record_btn_signal == True):
      self.record_button.setText('Stop Recording')
      self.record_btn_signal = False
      self.record_button.repaint()
      #self.t.init()
      self.t = Recorder.recorder()
      self.timevar.start()
      self.sema = threading.Thread(target=self.t.RECORDERfunc)
      self.sema.setDaemon(True)
      self.sema.start()


    elif (self.record_btn_signal == False):
      self.t.recsignal = False
      self.record_button.setText('Recording')
      self.record_button.repaint()
      self.record_btn_signal = True

      self.destroy()
  def printtime(self):
    self.time += 0.1
    self.textBrowser.setText('%s' %round(self.time,2))
    self.textBrowser.repaint()
    if(self.time > 5) :
      self.destroy()





class StatWindow(QMainWindow, form_class3):
  def __init__(self,parent = None):
    super(StatWindow, self).__init__(parent)
    self.setupUi(self)
    self.stat_exit_button.clicked.connect(self.stat_exit_btn_clicked)

  def stat_exit_btn_clicked(self):
    self.mainWindow3 = MainWindow()
    self.mainWindow3.show()
    self.destroy()


class TestWindow(QMainWindow, form_class2):
  def __init__(self, parent=None):
    super(TestWindow, self).__init__(parent)
    self.setupUi(self)
    self.test_record_button.clicked.connect(self.test_record_btn_clicked)
    self.test_next_button.clicked.connect(self.test_next_btn_clicked)
    self.test_exit_button.clicked.connect(self.test_exit_btn_clicked)
    self.test_result_button.clicked.connect(self.test_result_btn_clicked)
    a = randint(1, 4557)
    self.textBrowser.setText('%s' % text.loc[a, 0])
    self.test_result_button.setEnabled(False)
    self.txtdivide = StandardPro.standard()
    self.record_btn_signal = True
    self.test_next_button.setEnabled(False)
    for i in range(0, len(text.loc[a, 1])):
      self.txtdivide.divide(text.loc[a, 1][i])
    self.textBrowser_2.setText('%s' % self.txtdivide.letters[0].초성)
    self.textBrowser_3.setText('%s' % self.txtdivide.letters[0].중성)
    self.textBrowser_4.setText('%s' % self.txtdivide.letters[0].종성)
    if(len(text.loc[a, 0])>=2) :
      self.textBrowser_5.setText('%s' % self.txtdivide.letters[1].초성)
      self.textBrowser_6.setText('%s' % self.txtdivide.letters[1].중성)
      self.textBrowser_7.setText('%s' % self.txtdivide.letters[1].종성)
    if (len(text.loc[a, 0]) >= 3):
      self.textBrowser_2.setText('%s' % self.txtdivide.letters[0].초성)
      self.textBrowser_3.setText('%s' % self.txtdivide.letters[0].중성)
      self.textBrowser_4.setText('%s' % self.txtdivide.letters[0].종성)
      self.textBrowser_5.setText('%s' % self.txtdivide.letters[1].초성)
      self.textBrowser_6.setText('%s' % self.txtdivide.letters[1].중성)
      self.textBrowser_7.setText('%s' % self.txtdivide.letters[1].종성)
      self.textBrowser_8.setText('%s' % self.txtdivide.letters[2].초성)
      self.textBrowser_9.setText('%s' % self.txtdivide.letters[2].중성)
      self.textBrowser_10.setText('%s' % self.txtdivide.letters[2].종성)
    '''self.t=Recorder.recorder()
    self.sema = threading.Thread(target=self.t.RECORDERfunc)
    self.sema.setDaemon(True)'''

  def test_result_btn_clicked(self):
    print('결과창보기')
    self.test_result_button.setEnabled(False)
    self.test_record_button.setText('Recording')
    self.test_next_button.setEnabled(True)
    self.test_record_button.repaint()

  def test_record_btn_clicked(self):
    self.test_record_button.setText('Now Recordeing...')
    self.test_record_button.setEnabled(False)
    self.test_record_button.repaint()
    self.recordWindow = RecordWindow(self)
    self.recordWindow.show()
    self.test_result_button.setEnabled(True)
    self.test_result_button.repaint()


  def test_next_btn_clicked(self):
    self.test_record_button.setEnabled(True)
    a = randint(1, 4557)
    b = 0
    self.test_next_button.setEnabled(False)
    self.textBrowser.setText('%s' % text.loc[a, b])
    self.txtdivide = StandardPro.standard()
    for i in range(0, len(text.loc[a, 1])):
      self.txtdivide.divide(text.loc[a, 1][i])

    colorvar = QColor(255, 0, 0)
    self.textBrowser_2.setTextColor(colorvar)
    self.textBrowser_2.setText('%s' % self.txtdivide.letters[0].초성)
    self.textBrowser_3.setText('%s' % self.txtdivide.letters[0].중성)
    self.textBrowser_4.setText('%s' % self.txtdivide.letters[0].종성)
    if (len(text.loc[a, 0]) >= 2):
      self.textBrowser_5.setText('%s' % self.txtdivide.letters[1].초성)
      self.textBrowser_6.setText('%s' % self.txtdivide.letters[1].중성)
      self.textBrowser_7.setText('%s' % self.txtdivide.letters[1].종성)
      self.textBrowser_8.setText(' ')
      self.textBrowser_9.setText(' ')
      self.textBrowser_10.setText(' ')
    if (len(text.loc[a, 0]) >= 3):
      self.textBrowser_8.setText('%s' % self.txtdivide.letters[2].초성)
      self.textBrowser_9.setText('%s' % self.txtdivide.letters[2].중성)
      self.textBrowser_10.setText('%s' % self.txtdivide.letters[2].종성)


  def test_exit_btn_clicked(self):
    self.mainWindow2 = MainWindow()
    self.mainWindow2.show()
    self.destroy()



class TrainWindow(QMainWindow, form_class1):
  def __init__(self, parent=None):
    super(TrainWindow, self).__init__(parent)
    self.setupUi(self)
    self.train_record_button.clicked.connect(self.train_record_btn_clicked)
    self.train_next_button.clicked.connect(self.train_next_btn_clicked)
    self.train_exit_button.clicked.connect(self.train_exit_btn_clicked)
    self.train_result_button.clicked.connect(self.train_result_btn_clicked)
    a = randint(1, 4557)
    self.textBrowser.setText('%s' % text.loc[a, 0])
    self.train_result_button.setEnabled(False)
    self.record_btn_signal = True
    self.txtdivide = StandardPro.standard()
    self.train_next_button.setEnabled(False)
    for i in range(0, len(text.loc[a, 1])):
      self.txtdivide.divide(text.loc[a, 1][i])
    self.textBrowser_2.setText('%s' % self.txtdivide.letters[0].초성)
    self.textBrowser_3.setText('%s' % self.txtdivide.letters[0].중성)
    self.textBrowser_4.setText('%s' % self.txtdivide.letters[0].종성)
    if (len(text.loc[a, 0]) >= 2):
      self.textBrowser_5.setText('%s' % self.txtdivide.letters[1].초성)
      self.textBrowser_6.setText('%s' % self.txtdivide.letters[1].중성)
      self.textBrowser_7.setText('%s' % self.txtdivide.letters[1].종성)
    if (len(text.loc[a, 0]) >= 3):
      self.textBrowser_2.setText('%s' % self.txtdivide.letters[0].초성)
      self.textBrowser_3.setText('%s' % self.txtdivide.letters[0].중성)
      self.textBrowser_4.setText('%s' % self.txtdivide.letters[0].종성)
      self.textBrowser_5.setText('%s' % self.txtdivide.letters[1].초성)
      self.textBrowser_6.setText('%s' % self.txtdivide.letters[1].중성)
      self.textBrowser_7.setText('%s' % self.txtdivide.letters[1].종성)
      self.textBrowser_8.setText('%s' % self.txtdivide.letters[2].초성)
      self.textBrowser_9.setText('%s' % self.txtdivide.letters[2].중성)
      self.textBrowser_10.setText('%s' % self.txtdivide.letters[2].종성)




  def train_result_btn_clicked(self):
    print('결과창보기')
    self.train_result_button.setEnabled(False)
    self.train_record_button.setText('Recording')

    self.train_next_button.setEnabled(True)
    self.train_record_button.repaint()

  def train_record_btn_clicked(self):
    self.train_record_button.setText('Now Recordeing...')
    self.train_record_button.setEnabled(False)
    self.train_record_button.repaint()
    self.recordWindow = RecordWindow(self)
    self.recordWindow.show()
    self.train_result_button.setEnabled(True)
    self.train_result_button.repaint()

  def train_next_btn_clicked(self):
    a = randint(1, 4557)
    b = 0
    self.train_record_button.setEnabled(True)
    self.train_next_button.setEnabled(False)
    self.textBrowser.setText('%s' % text.loc[a, b])
    self.txtdivide = StandardPro.standard()
    for i in range(0, len(text.loc[a, 1])):
      self.txtdivide.divide(text.loc[a, 1][i])

    self.textBrowser_2.setText('%s' % self.txtdivide.letters[0].초성)
    self.textBrowser_3.setText('%s' % self.txtdivide.letters[0].중성)
    self.textBrowser_4.setText('%s' % self.txtdivide.letters[0].종성)
    if (len(text.loc[a, 0]) >= 2):
      self.textBrowser_5.setText('%s' % self.txtdivide.letters[1].초성)
      self.textBrowser_6.setText('%s' % self.txtdivide.letters[1].중성)
      self.textBrowser_7.setText('%s' % self.txtdivide.letters[1].종성)
      self.textBrowser_8.setText(' ')
      self.textBrowser_9.setText(' ')
      self.textBrowser_10.setText(' ')
    if (len(text.loc[a, 0]) >= 3):
      self.textBrowser_8.setText('%s' % self.txtdivide.letters[2].초성)
      self.textBrowser_9.setText('%s' % self.txtdivide.letters[2].중성)
      self.textBrowser_10.setText('%s' % self.txtdivide.letters[2].종성)

  def train_exit_btn_clicked(self):
    self.mainWindow = MainWindow()
    self.mainWindow.show()
    self.destroy()


class MainWindow(QMainWindow, form_class):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.testbutton.clicked.connect(self.testbtn_clicked)
    self.trainbutton.clicked.connect(self.trainbtn_clicked)
    self.statbutton.clicked.connect(self.statbtn_clicked)
    self.exitbutton.clicked.connect(self.exitbtn_clicked)


  def testbtn_clicked(self):
    self.testWindow = TestWindow(self)
    self.testWindow.show()
    self.destroy()

  def trainbtn_clicked(self):
    self.trainWindow = TrainWindow(self)
    self.trainWindow.show()
    self.destroy()
  def statbtn_clicked(self):
    self.statWindow = StatWindow(self)
    self.statWindow.show()
    self.destroy()
  def exitbtn_clicked(self):
    sys.exit()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
'''
import pyaudio

po = pyaudio.PyAudio()

for index in range(po.get_device_count()):

    desc = po.get_device_info_by_index(index)

    #if desc["name"] == "record":

    print("DEVICE: %s  INDEX:  %s  RATE:  %s " % (desc["name"], index,  int(desc["defaultSampleRate"])))
'''