import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '\\source')
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '\\source\\PhonemeModule')
from UI.MainWindow import MainWindow
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
