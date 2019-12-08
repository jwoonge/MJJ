import pandas as pd
from random import *
import os
#import StandardPro


def Readcsv():
  quizbankpath = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/resource/CSV source/'
  src = pd.read_csv(quizbankpath + 'QuizBank.csv', encoding='CP949', header=None)

  return src


