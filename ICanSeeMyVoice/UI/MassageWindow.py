import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView
from random import *

import time



uipath = os.path.abspath(os.path.dirname(__file__)) + '/UI resource/MASSAGE_UI.ui'
form_class1 = uic.loadUiType(uipath)[0]


class MassageWindow(QMainWindow, form_class1):
  def __init__(self, parent=None):
    super(MassageWindow, self).__init__(parent)
    self.setupUi(self)
    self.OKbutton.clicked.connect(self.Massage_OK_btn_clicked)

  def Massage_OK_btn_clicked(self):
    self.destroy()
