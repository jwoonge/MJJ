import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView
from random import *

import time



uipath = os.path.abspath(os.path.dirname(__file__)) + '/UI resource/RESULT_UI.ui'
form_class1 = uic.loadUiType(uipath)[0]


class ResultWindow(QMainWindow, form_class1):
  def __init__(self, parent=None):
    super(ResultWindow, self).__init__(parent)
    self.setupUi(self)
    self.ExitButton.clicked.connect(self.Exit_btn_clicked)

  def Exit_btn_clicked(self):

    self.destroy()
