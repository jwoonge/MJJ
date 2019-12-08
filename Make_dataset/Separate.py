from PhonemeProc import PhonemeProc
import sys
import os
from collections import namedtuple

##################################################
##################################################

Proc = PhonemeProc()
TotHitCount = 0
Directory = "../Todo"
#Directory = '../../dataset'
folders_Done = []
folders_Todo = []

for i in os.listdir(Directory):
    if not '.' in i and not 'MJJ' in i :
        folders_Todo.append(i)

while(len(folders_Todo)>0):
    Dir_folder = Directory + '/' + folders_Todo[0]
    print(folders_Todo[0],' start')
    files = os.listdir(Dir_folder)
    HitCount = 0
    filenames = []
    for file in files:
        if '.pcm' in file:
            temp_file = file.split('.')
            filenames.append(temp_file[0])
    for filename in filenames:
        Dir_file = Dir_folder + '/' + filename
        Phonemes = Proc.DoProcess(Dir_file)
        if Phonemes > 0:
            HitCount += 1
            print("\tfile : ", filename, "\tHIT ",Phonemes)
        else:
            print("\tfile : ", filename, "\tMISS")
    print("   folder : ", folders_Todo[0], '\tHitCount : ', HitCount)
    TotHitCount += HitCount

    folders_Done.append(folders_Todo[0])
    folders_Todo = []
    for i in os.listdir(Directory):
        if (not '.' in i) and (not 'MJJ' in i) and (not i in folders_Done) :
            folders_Todo.append(i)

print("Dataset Making finished. Total Hit : ",TotHitCount)
print(folders_Done)