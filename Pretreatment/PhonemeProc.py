from PCMdata import PCMdata
import RWwav
import Framing
from collections import namedtuple
import Calculator as c
import SoundVisualization as sv

class PhonemeProc():
    def __init__(self, _frame_size=512, _interval=480, _sensitivity=27, _frame_size_d=32,_interval_d=30):
        self.frame_size= _frame_size
        self.interval = _interval
        self.sensitivity = _sensitivity
        self.frame_size_d = _frame_size_d
        self.interval_d = _interval_d


    def Separating(self, input_str):
        self.pcm = RWwav.Read_file(input_str, self.frame_size, self.interval)
        RWwav.Write_wav("origin.wav",self.pcm.value,self.pcm.Fs)
        self.pcm_framed = Framing.Framing(self.pcm.value, self.frame_size, self.interval)
        # sv.Show_Soundwave(pcm.value)
        self.frame_table = []
        for i in range(len(self.pcm_framed)):
            temp = namedtuple('Coordinate',['Empty','Convex'])
            temp.Empty = False
            temp.Convex = 'None'
            self.frame_table.append(temp)
        self.frame_LE = c.Log_Energy(self.pcm_framed)
        #### mark empty ####
        self.Mark_Empty()
        self.Check_Empty()
        RWwav.Write_wav("removed.wav",self.Removed_empty,self.pcm.Fs)

        #### remove empty ####
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
        self.frame_LE_removed_framed = Framing.Framing(self.frame_LE_removed,self.frame_size_d,self.interval_d)
        self.logSpec = c.Spectrogram(self.frame_LE_removed_framed, self.pcm.Fs)
        self.inverted_logSpec = []
        for j in range(len(self.logSpec[0])):
            temp = []
            for i in range(len(self.logSpec)):
                temp.append(self.logSpec[i][j])
            self.inverted_logSpec.append(temp)
        
        #### mark convex ####
        self.Mark_Convex()
        ##################################################
        self.Separating_write("Separated")
        sv.Show_Array(self.inverted_logSpec[0])
        sv.Show_Array(self.inverted_logSpec[1])
 
    def Separating_write(self, fileDir, cutting_sec=0.05):
        print(RWwav.removeAllFile(fileDir))
        cutting_range = int(cutting_sec * self.pcm.Fs)
        number = 1
        for i in range(len(self.frame_table)):
            if (not self.frame_table[i].Convex == 'None'):
                #print(i)
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
        minLenSect = (0.12 * self.pcm.Fs - self.frame_size) / (self.frame_size - self.interval)
        # have to modify minLenF
        start = 0
        end = start
        while(end < len(self.frame_table)):
            end = start
            if end<len(self.frame_table) and self.frame_table[end].Empty == False:
                while(end<len(self.frame_table) and self.frame_table[end+1].Empty == False):
                    end += 1
            lenSect = end - start

            if lenSect < minLenSect:
                for i in range(start, end+1):
                    if i<len(self.frame_table):
                        self.frame_table[i].Empty = True
                        print("Noise Removed")
            
            start = end + 1

    def Mark_Convex(self):

        ####### calculate inclinations #######
        inclinations = []
        for i in range(2):
            temp = []
            for j in range(len(self.inverted_logSpec[i])-1):
                inclination = self.inverted_logSpec[i][j+1]-self.inverted_logSpec[i][j]
                temp.append(inclination)
            inclinations.append(temp)

        ####### get points from freq0 Graph #######
        points_0 = []
        inflections_0 = []
        for i in range(len(inclinations[0])-1):
            if(inclinations[0][i+1]*inclinations[0][i]<=0):
                inflections_0.append(i)
        print('0: ',inflections_0)
        start = 0
        end = start
        while end<len(inflections_0)-1 :
            end = start
            while(end<(len(inflections_0)-1)) and abs(inflections_0[end+1]-inflections_0[end])<=5:
                end += 1
            pointIndex = start
            preStart = inflections_0[start]-1
            postEnd = inflections_0[end]+1
            Valid = True
            state = None
            if preStart < 0:
                preStart = 0
            if postEnd >= len(inclinations[0]):
                postEnd = len(inclinations[0])-1
            
            if( inclinations[0][preStart] >= 0 and inclinations[0][postEnd]< 0 ):
                state = 'Concave_0'
                Max = self.inverted_logSpec[0][start]
                for i in range(start,end+1):
                    if(self.inverted_logSpec[0][inflections_0[i]]>Max):
                        Max = self.inverted_logSpec[0][inflections_0[i]]
                        pointIndex = i

            elif( inclinations[0][preStart] < 0 and inclinations[0][postEnd] >= 0):
                state = 'Convex_0'
                Min = self.inverted_logSpec[0][start]
                for i in range(start,end+1):
                    if(self.inverted_logSpec[0][inflections_0[i]]<Min):
                        Min = self.inverted_logSpec[0][inflections_0[i]]
                        pointIndex = i
                if self.inverted_logSpec[0][inflections_0[pointIndex]]<0.02:
                    Valid = False
                    print("deleted one by Under_values")

            else:
                state = 'Stable_0'
                zero = inclinations[0][inflections_0[start]]
                for i in range(start, end+1):
                    if (abs(inclinations[0][inflections_0[i]])<abs(zero)):
                        zero = inclinations[0][inflections_0[i]]
                        pointIndex = i
            if Valid==True:
                temp = namedtuple('Coordinate',['point', 'state'])
                temp.point = inflections_0[pointIndex] + 1
                temp.state = state
                points_0.append(temp)
            start = end + 1
        points_0_points = []
        for i in range(len(points_0)):
            points_0_points.append(points_0[i].point)
        ####### get points from freq1 graph #######

        points_1 = []
        inflections_1 = []
        for i in range(len(inclinations[1])-1):
            if(inclinations[1][i+1]*inclinations[1][i]<=0):
                inflections_1.append(i)
        print('1: ',inflections_1)
        start = 0
        end = start
        while end<len(inflections_1)-1 :
            state = 'None'
            Valid = True
            end = start
            while(end<(len(inflections_1)-1)) and abs(inflections_1[end+1]-inflections_1[end])<=5:
                end+=1
                ## 이 시점에 start, end 결정됨

            pointIndex = start
            preStart = inflections_1[start]-1
            postEnd = inflections_1[end]+1
            
            if preStart < 0:
                preStart = 0
            if postEnd >= len(inclinations[1]):
                postEnd = len(inclinations[1])-1
            
            for i in range(preStart-2, postEnd+2):
                if i in points_0_points:
                    Valid = False
            
            for i in range(start, end+1):
                if self.inverted_logSpec[1][inflections_1[i]]<0.02:
                    Valid = False
                    print("removed by value under 0.02")

            if Valid==True:
                if( inclinations[1][preStart] < 0 and inclinations[1][postEnd] >= 0):
                    state = 'Convex_1'
                    Min = self.inverted_logSpec[1][start]
                    for i in range(start,end+1):
                        if(self.inverted_logSpec[1][inflections_1[i]]<Min):
                            Min = self.inverted_logSpec[1][inflections_1[i]]
                            pointIndex = i
                    if self.inverted_logSpec[1][inflections_1[pointIndex]]<0.02:
                        Valid = False

                elif ( inclinations[1][preStart] * inclinations[1][postEnd] >= 0):
                    state = 'Stable_1'
                    zero = inclinations[1][inflections_1[start]]
                    for i in range(start, end+1):
                        if (abs(inclinations[1][inflections_1[i]])<abs(zero)):
                            zero = inclinations[1][inflections_1[i]]
                            pointIndex = i

                else:
                    Valid = False

            if Valid==True:
                temp = namedtuple('Coordinate',['point', 'state'])
                temp.point = inflections_1[pointIndex] + 1
                temp.state = state
                points_1.append(temp)
            start = end + 1

        points = points_0 + points_1
        points = sorted(points, key = lambda x:x.point)

        lst_count= 0
        for i in range(points[len(points)-2].point+1, points[len(points)-1].point):
            if inclinations[0][i]>=0:
                lst_count+=1
        if lst_count == 0:
            temp = []
            for i in range(len(points)-1):
                temp.append(points[i])
            points = temp
            print("Removed last points")
        ### mark Convex of frame_table ###
        for i in range(len(points)):
            print(i+1," ",points[i].point," ",points[i].state)
            index_from_frame_d = Framing.Index_frame_to_origin(points[i].point,self.frame_size_d,self.interval_d)
            index_from_frame_d += int(self.frame_size_d/2)
            index_from_frame_rm = self.invert_frame_table[index_from_frame_d]
            if index_from_frame_rm < len(self.frame_table)-2:
                self.frame_table[index_from_frame_rm].Convex = points[i].state
            else:
                print('Index out of range in Mack_Convex')



