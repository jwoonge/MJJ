from PCMdata import PCMdata
import RWwav
import Framing
from collections import namedtuple
import Calculator as c
import SoundVisualization as sv
from StandardPro import standard
import sys

class PhonemeProc():
    def __init__(self, _sensitivity=30):
        self.sensitivity = _sensitivity
        self.StandardProc = standard()

    def Directory_Make(self, fileNo = 0, filename_first = 'input/KsponSpeech_'):
        filename_second = ''

        if fileNo < 10:
	        filename_second = '00000' + str(fileNo)
        elif fileNo < 100:
            filename_second = '0000' + str(fileNo)
        elif fileNo < 1000:
            filename_second = '000' + str(fileNo)
        elif fileNo < 10000:
            filename_second = '00' + str(fileNo)
        elif fileNo < 100000:
            filename_second = '0' + str(fileNo)
        else:
            filename_second = str(fileNo)
        filename = filename_first + filename_second

        return filename

    def Separating(self, fileNo = 0, fileDir = "Default", pcmwav = "pcm"):
        if fileNo == 0:
            self.fileNo = 1
        else:
            self.fileNo = fileNo
        self.Hit = False
        if fileDir=="Default":
            Directory = self.Directory_Make(fileNo)
        else:
            Directory = fileDir
        self.StandardProc.fileread(Directory)
        self.Pronun = self.StandardProc.getPronunciation()

        self.pcm = RWwav.Read_file(Directory+'.'+pcmwav)
        self.frame_size = int((self.pcm.Fs / 12000) * 512)
        self.interval = int((self.pcm.Fs / 12000) * 480)
        self.frame_size_d = int((self.pcm.Fs / 16000) * 32)
        self.interval_d = self.frame_size_d-2
        #RWwav.Write_wav("origin.wav",self.pcm.value,self.pcm.Fs)
        self.pcm_framed = Framing.Framing(self.pcm.value, self.frame_size, self.interval)
        # sv.Show_Soundwave(pcm.value)
        self.frame_table = []
        for i in range(len(self.pcm_framed)):
            temp = namedtuple('Coordinate',['Empty','Convex','Hit'])
            temp.Empty = False
            temp.Convex = 'None'
            temp.Hit = False
            self.frame_table.append(temp)
        self.frame_LE = c.Log_Energy(self.pcm_framed)
        #### mark empty ####
        #print("Mark Empty")
        self.Mark_Empty()
        self.Check_Empty()
        #RWwav.Write_wav("removed.wav",self.Removed_empty,self.pcm.Fs)

        #### remove empty ####
        #print("Remove Empty")
        self.frame_LE_removed = []
        self.pcm_framed_removed = []
        self.invert_frame_table = [] #index of framed_removed -> index of framed
        for i in range(len(self.frame_table)):
            if not self.frame_table[i].Empty:
                self.pcm_framed_removed.append(self.pcm_framed[i])
                self.invert_frame_table.append(i)
                self.frame_LE_removed.append(self.frame_LE[i])
        # sv.Show_Array(self.frame_LE_removed)
        #################################################
        #print('Calc inverted_LogSpectrogram')
        self.frame_LE_removed_framed = Framing.Framing(self.frame_LE_removed,self.frame_size_d,self.interval_d)
        self.logSpec = c.Spectrogram(self.frame_LE_removed_framed, self.pcm.Fs)
        self.inverted_logSpec = []
        for j in range(len(self.logSpec[0])):
            temp = []
            for i in range(len(self.logSpec)):
                temp.append(self.logSpec[i][j])
            self.inverted_logSpec.append(temp)
    
        #### mark convex #################################
        #print('Mark Convex')
        self.Mark_Convex()
        ##################################################
        #print('Calc Hit')
        self.Mark_Hit()

        #################################################
        #print('Separate')
        if self.Hit:
            self.Separating_write("Separated")

        return self.Hit
        
        
    def Mark_Hit(self):
        HitCount = 0
        for i in range(len(self.frame_table)):
            if not self.frame_table[i].Convex=='None':
                self.frame_table[i].Hit = True
                HitCount += 1
        if HitCount == len(self.Pronun):
            self.Hit = True
            print("HIT")
            for i in range(len(self.points)):
                print(i+1,"\t",self.points[i].point,"\t",self.points[i].state, "\t", self.Pronun[i])
        else:
            self.Hit = False
            print(self.fileNo,"\tMISS\t HitCount : ",HitCount,"\tExpected : ",len(self.Pronun))
 
    def Separating_write(self, fileDir, cutting_sec=0.05):
        RWwav.removeAllFile(fileDir)
        cutting_range = int(cutting_sec * self.pcm.Fs)
        number = 1
        for i in range(len(self.frame_table)):
            if (self.frame_table[i].Hit):
                directory = fileDir + '/' + str(number) + '.wav'
                number += 1
                WriteList = []
                mid = Framing.Index_frame_to_origin(i,self.frame_size,self.interval) + int((self.frame_size)/2)
                if (mid-int(cutting_range*0.5) > 0) and (mid+int(cutting_range*0.5)-1 < self.pcm.value_count):
                    for j in range(cutting_range):
                        if (mid - int(cutting_range*0.5)+j < self.pcm.value_count):
                            WriteList.append(self.pcm.value[mid-int(cutting_range*0.5)+j])
                        else:
                            print('Index out of range in Separating_Write')
                RWwav.Write_wav(directory, WriteList, self.pcm.Fs)
        
    
    def Mark_Empty(self):
        maxE = max(self.frame_LE)
        for i in range(len(self.frame_table)):
            if self.frame_LE[i] < (self.sensitivity/100) * maxE:
                self.frame_table[i].Empty = True
        for i in range(len(self.frame_table)-2):
            if self.frame_table[i].Empty and (not self.frame_table[i+1]) and self.frame_table[i+2] :
                self.frame_table[i+1] = False

        
        markData = [1 for i in range((self.frame_size-self.interval)*(len(self.pcm_framed)-1)+self.frame_size)]
        for i in range(len(self.pcm_framed)):
            if self.frame_table[i].Empty:
                for j in range(self.frame_size):
                    markData[(self.frame_size-self.interval)*i+j]=0
        self.Removed_empty = []
        for i in range(len(markData)):
            if markData[i]==1 and i<self.pcm.value_count:
                self.Removed_empty.append(self.pcm.value[i])

    def Check_Empty(self):
        minLenSect = int((0.12 * self.pcm.Fs - self.frame_size) / (self.frame_size - self.interval))
        # have to modify minLenF
        start = 0
        end = start
        while(end < len(self.frame_table)):
            end = start
            if end<len(self.frame_table) and self.frame_table[end].Empty == False:
                while(end<len(self.frame_table)-1 and self.frame_table[end+1].Empty == False):
                    end += 1
            lenSect = end - start

            if lenSect < minLenSect:
                for i in range(start, end+1):
                    if i<len(self.frame_table):
                        self.frame_table[i].Empty = True
            
            start = end + 1

    def Mark_Convex(self):
        self.points = []
        points_0 = c.GetConvex(self.inverted_logSpec[0])
        #print('points 0 calculated')
        points_1 = c.GetConvex(self.inverted_logSpec[1])
        #print('points 1 calculated')
        for i in range(len(points_0)):
            self.points.append(points_0[i])
        for i in range(len(points_1)):
            if points_1[i].state == 'Convex' or points_1[i].state == 'Stable':
                Remove = False
                for j in range(len(points_0)):
                    if abs(points_1[i].point - points_0[j].point)<10:
                        Remove = True
                        break
                if not Remove:
                    self.points.append(points_1[i])            
       
        self.points = sorted(self.points, key = lambda x:x.point)

        ### mark Convex of frame_table ###
        
        for i in range(len(self.points)):
            index_from_frame_d = Framing.Index_frame_to_origin(self.points[i].point,self.frame_size_d,self.interval_d)
            index_from_frame_d += int(self.frame_size_d/2)
            index_from_frame_rm = self.invert_frame_table[index_from_frame_d]
            if index_from_frame_rm < len(self.frame_table)-2:
                self.frame_table[index_from_frame_rm].Convex = self.points[i].state
            else:
                print('Index out of range in Mark_Convex')
