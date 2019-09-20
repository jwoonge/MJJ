import pandas as pd
from random import *

def Readcsv() :
  src = pd.read_csv('C:\\Users\\JooHwan\\PycharmProjects\\GUI\\venv\CSV source\QuizBank.csv', engine= 'python')
  i = randint(0, 2)
  Readstring = src.columns[i]
  return Readstring
