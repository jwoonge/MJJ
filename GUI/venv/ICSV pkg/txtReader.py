import pandas as pd
from random import *
#import StandardPro


def Readcsv():
  src = pd.read_csv('/home/pi/Desktop/venv/CSV source/QuizBank.csv', encoding='CP949', header=None)

  return src


