import pandas as pd
from random import *
#import StandardPro


def Readcsv():
  src = pd.read_csv('/home/pi/Desktop/ICanSeeMyVoice/CSV source/QuizBank.csv', encoding='CP949', header=None)

  return src


<<<<<<< HEAD
def Readcsv() :
  src = pd.read_csv('CSV source\QuizBank.csv', engine= 'python')
  i = randint(0, 2)
  Readstring = src.columns[i]
  return Readstring
=======
>>>>>>> GUI
