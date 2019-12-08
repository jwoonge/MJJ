import RWwav
import Framing
from collections import namedtuple
import Calculator as c
from StandardPro import standard
import sys
import python_speech_features as psf
import numpy as np
import csv
import math
from scipy.ndimage import filters

class PhonemeProc():
    def __init__(self):
        self.StandardProc=standard()


    def DoProcess(self, filename):
        self.Settings(filename)
        if not self.file_valid:
            return 0

        self.Spec = c.Spectrogram(self.pcm_framed, self.sample_rate)
        self.Mark_Empty()
        self.Mark_UV()
        self.Check_Empty_UV()
        self.UV_list = self.UV_Section()
        self.g = filters.gaussian_filter1d(c.GetInclinations_abs(filters.gaussian_filter1d(self.frame_LE,0.1)),2.5)
        self.g_inc = c.GetInclinations(self.g)
        self.Separate()
        self.Make_dataset()
        
        return len(self.phonemes)

    def Separate(self):
        self.phonemes = []

        ### Case 1 : best case - UV detected successfully ###
        if len(self.UV_list)==len(self.UV_txt):
            for i in range(len(self.UV_list)):
                points = self.Get_Points_from_Sector(self.UV_list[i].start, self.UV_list[i].end, len(self.UV_txt[i]), self.UV_list[i].UV)
                for j in range(len(points)):
                    temp = namedtuple('phoneme',['point','label','pcm_start','pcm_end'])
                    temp.point = points[j]
                    temp.label = self.UV_txt[i][j]
                    if temp.label != 'S':
                        self.phonemes.append(temp)

        ### Case 2 : Number of Phonemes from whole sector is matched with Expected ###

        ### Case 3 : worst case - Timing matching
        
        ### PostTreat : calculate p_start, p_end
        for i in range(len(self.phonemes)):
            f_start = Framing.Index_frame_to_origin(self.phonemes[i].point,self.frame_size,self.interval)
            f_end = f_start + 2 * self.frame_size - self.interval
            f_range = (f_start-f_end)
            sectlen = int(0.05*self.sample_rate)
            #p_start = f_start - int((sectlen-f_range)/2)
            #p_end = p_start + sectlen
            p_start = f_start - int((sectlen-f_range)/2) + 650
            
            if p_start < 0 :
                p_start = 0
            
            p_end = p_start + sectlen
            
            if p_end >= len(self.pcm):
                p_end = len(self.pcm)-1
                p_start = p_end - sectlen
            
            self.phonemes[i].pcm_start = p_start
            self.phonemes[i].pcm_end = p_end


    def Get_Points_from_Sector(self, start, end, n, UV):
        ### from the sector in range(start, end), return N points as list of integer ###
        points = []
        
        if UV=='V':
            every_convex = c.GetConvex_range(self.g_inc,start,end)
            if len(every_convex)>n:
                convexes = []
                for i in range(len(every_convex)):
                    temp = namedtuple('points',['x','y'])
                    temp.x = every_convex[i]
                    temp.y=self.g[every_convex[i]]
                    convexes.append(temp)
                
                convexes = sorted(convexes, key=lambda x:x.y)
                for i in range(n):
                    points.append(convexes[i].x)

            elif len(every_convex)==n:
                points += every_convex            

        elif UV=='U':
            if n==1:
                Min = self.g[start]
                MinX = start
                for i in range(start,end):
                    if not self.frame_table[i].Empty and Min > self.g[i]:
                        Min = self.g[i]
                        MinX = i
                points.append(MinX)
            elif n==2:
                empty_start = start
                empty_end = end
                for i in range(start,end-1):
                    if not self.frame_table[i].Empty and self.frame_table[i+1].Empty:
                        empty_start = i+1
                    if self.frame_table[i].Empty and not self.frame_table[i+1].Empty:
                        empty_end = i

                points += self.Get_Points_from_Sector(start,empty_start,1,'U')
                points += self.Get_Points_from_Sector(empty_end+1,end,1,'U')

        return sorted(points)


    def UV_Section(self):
        ret=[]
        ret2=[]
        start=0
        i = 0
        end = 0
        temp = self.frame_table[0].UV
        while i < len(self.frame_table):
            Value = namedtuple("UV_Segment", ['start', 'end', 'UV'])
            j = i
            while j < len(self.frame_table):
                if temp != self.frame_table[j].UV:
                    Value.UV = temp
                    temp = self.frame_table[j].UV
                    end = j
                    Value.start = start
                    Value.end = end
                    start = j
                    ret.append(Value)
                    j+=1
                    break
                j+=1
                #count+=1
            i =j

        i = 0
        while i < len(ret)-1 :
            if i == 0 and ret[i].UV==0:
                i+=1
                continue
            if ret[i].UV == 0 :
                ret[i-1].end = ret[i+1].end
                ret[i+1].UV = 0
                i += 1
            i += 1

        for i in range(len(ret)) :
            if ret[i].UV == 2 :
                ret[i].UV = 'U'
            elif ret[i].UV == 3 :
                ret[i].UV = 'V'
       
        for i in range(len(ret)) :
            if ret[i].UV != 0 :
                ret2.append(ret[i])

        return ret2

    def Mark_Empty(self):
        Spect = self.Spec

        self.maxes = []
        for i in range(len(self.frame_table)):
            self.maxes.append(max(Spect[i]))
        OptMax = max(self.maxes)
        LEMax = max(self.frame_LE)
        for i in range(len(self.frame_table)):
            if max(Spect[i]) < OptMax/1000:
                self.frame_table[i].Empty = True
            if self.frame_LE[i] < 0.2 * LEMax:
                self.frame_table[i].Empty = True

    def Mark_UV(self):
        Spect = self.Spec

        ### 무게중심 y가 max의 10%이상이면 유성음 ###
        centerY = c.GetCenterOfMass(Spect,'y')
        th_center = max(centerY)/10

        for i in range(len(self.frame_table)):
            if centerY[i] > th_center:
                self.frame_table[i].UV = 3
            else:
                if not self.frame_table[i].Empty:
                    self.frame_table[i].UV = 2
        
        ### 180 이상인 것들이 12개 이상 있으면 유성음 ###
        th_max = 180
        for i in range(len(Spect)):
            count = 0
            for j in range(len(Spect[i])):
                if Spect[i][j]> th_max:
                    count += 1
            if count > self.frame_size / 40:
                self.frame_table[i].UV = 3

        ### max가 1000 이상인 프레임은 유성음 ###
        for i in range(len(self.frame_table)):
            if self.maxes[i] > 1000:
                self.frame_table[i].UV = 3
        

    def Check_Empty_UV(self):
        ## Check UV line with time ##
        
        minVlen = int((0.05 * self.sample_rate - self.frame_size) / (self.frame_size - self.interval))
        start = 0
        end = start
        while(end < len(self.frame_table)):
            end = start
            if end<len(self.frame_table) and self.frame_table[end].UV == 3:
                while end<len(self.frame_table)-1 and self.frame_table[end+1].UV == 3:
                    end += 1
            lenSect = end-start
            if lenSect < minVlen:
                for i in range(start, end+1):
                    if i<len(self.frame_table) and not self.frame_table[i].Empty:
                        self.frame_table[i].UV = 2
            start = end + 1
        
        
        ## Check /b or noise by _U_
        points=[] #points : 무음->유음, 유음->무음 가는 지점들
        if not self.frame_table[0].Empty:
            points.append(0)
        for i in range(len(self.frame_table)-1):
            if self.frame_table[i].Empty and not self.frame_table[i+1].Empty:
                points.append(i+1)
            elif not self.frame_table[i].Empty and self.frame_table[i+1].Empty:
                points.append(i+1)
        if not self.frame_table[-1].Empty:
            points.append(len(self.frame_table)-1)
        
        for i in range(len(points)-1):
            start=points[i]
            end=points[i+1]
            countV=0
            for j in range(start, end):
                if self.frame_table[j].UV==3:
                    countV +=1
            if countV==0: # not exist V sound in range(start,end)
                for j in range(start, end):
                    self.frame_table[j].Empty=True
                    self.frame_table[j].UV=0
            i +=1
        

        ## Check VU_ _UV _V V_
        #3-2-0, 0-2,3 인 2구간을 찾아야해
        start = 0
        end = 0
        for i in range(len(self.frame_table)-1):
            if self.frame_table[i].UV-self.frame_table[i+1].UV==2: #U->N
                end = i + 1 # end : 0이 처음 된 지점
                start = end - 1
                while self.frame_table[start]==2:
                    start -= 1
                start += 1
                '''
                if start~end 어떤 그래프 기울기가 계속 감소하면
                    그 구간은 전부다 3
                '''


            elif self.frame_table[i].UV-self.frame_table[i+1].UV==-2: #N->U
                start = i + 1 # start : 2가 처음 된 지점
                end = start
                while self.frame_table[end]==2:
                    end += 1
                '''
                if start~end... 증가하면
                    그 구간 전부 3
                '''

    def Settings(self, filename):
        self.StandardProc.fileread(filename)
        self.Pronun=self.StandardProc.getPronunciation()
        self.UV_txt = self.StandardProc.getIsVoiced()

        self.file_valid = self.StandardProc.getFileValid()

        self.pcm, self.sample_rate = RWwav.Read_file(filename+'.pcm')
        self.frame_size=int((self.sample_rate / 16000) * 512)
        self.interval=int((self.sample_rate / 16000) * 480)

        self.maskW=5
        self.maskH=3
        self.mask=[]
        for i in range(self.maskW):
            mask_tmp=[]
            for j in range(self.maskH):
                mask_tmp.append(1)
            self.mask.append(mask_tmp)

        self.Framing_pcm()

    def Framing_pcm(self):
        self.pcm_framed=Framing.Framing(self.pcm, self.frame_size, self.interval)
        self.frame_table=[]
        for i in range(len(self.pcm_framed)):
            temp=namedtuple('Status', ['Empty', 'UV'])
            temp.Empty=False
            temp.UV=0
            self.frame_table.append(temp)
        self.frame_LE=c.Log_Energy(self.pcm_framed)

    def Make_dataset(self):
        output_file = open("MFCC.csv","a",newline="")
        writer = csv.writer(output_file)
        for i in range(len(self.phonemes)):
            WriteList = self.pcm[self.phonemes[i].pcm_start: self.phonemes[i].pcm_end]
            Label =1
            mfcclist = []
            mfccWriteList = np.array(WriteList)
            temp = psf.mfcc(mfccWriteList, samplerate=self.sample_rate, winlen=0.01,winstep=0.01, nfft=self.frame_size, numcep=12)
            for k in range(temp.shape[0]):
                templist = []
                for j in range(temp.shape[1]):
                    templist.append(temp[k][j])
                mfcclist.append(templist)

            if self.phonemes[i].label == 'ㄱ':
                Label = 1
            elif self.phonemes[i].label == 'ㄴ':
                Label = 2
            elif self.phonemes[i].label == 'ㄷ':
                Label = 3
            elif self.phonemes[i].label == 'ㄹ':
                Label = 4
            elif self.phonemes[i].label == 'ㅁ':
                Label = 5
            elif self.phonemes[i].label == 'ㅂ':
                Label = 6
            elif self.phonemes[i].label == 'ㅅ':
                Label = 7
            elif self.phonemes[i].label == 'ㅇ':
                Label = 8
            elif self.phonemes[i].label == 'ㅈ':
                Label = 9
            elif self.phonemes[i].label == 'ㅊ':
                Label = 10
            elif self.phonemes[i].label == 'ㅋ':
                Label = 11
            elif self.phonemes[i].label == 'ㅌ':
                Label = 12
            elif self.phonemes[i].label == 'ㅍ':
                Label = 13
            elif self.phonemes[i].label == 'ㅎ':
                Label = 14
            elif self.phonemes[i].label == 'ㄲ':
                Label = 15
            elif self.phonemes[i].label == 'ㄸ':
                Label = 16
            elif self.phonemes[i].label == 'ㅃ':
                 Label = 17
            elif self.phonemes[i].label == 'ㅆ':
                Label = 18
            elif self.phonemes[i].label == 'ㅉ':
                Label = 19
            elif self.phonemes[i].label == 'ㅏ':
                Label = 20
            elif self.phonemes[i].label == 'ㅐ':
                Label = 21
            elif self.phonemes[i].label == 'ㅑ':
                Label = 22
            elif self.phonemes[i].label == 'ㅒ':
                Label = 23
            elif self.phonemes[i].label == 'ㅓ':
                Label = 24
            elif self.phonemes[i].label == 'ㅔ':
                Label = 25
            elif self.phonemes[i].label == 'ㅕ':
                Label = 26
            elif self.phonemes[i].label == 'ㅖ':
                Label = 27
            elif self.phonemes[i].label == 'ㅗ':
                Label = 28
            elif self.phonemes[i].label == 'ㅘ':
                Label = 29
            elif self.phonemes[i].label == 'ㅙ':
                Label = 30
            elif self.phonemes[i].label == 'ㅚ':
                Label = 31
            elif self.phonemes[i].label == 'ㅛ':
                Label = 32
            elif self.phonemes[i].label == 'ㅜ':
                Label = 33
            elif self.phonemes[i].label == 'ㅝ':
                Label = 34
            elif self.phonemes[i].label == 'ㅞ':
                Label = 35
            elif self.phonemes[i].label == 'ㅟ':
                Label = 36
            elif self.phonemes[i].label == 'ㅠ':
                Label = 37
            elif self.phonemes[i].label == 'ㅡ':
                Label = 38
            elif self.phonemes[i].label == 'ㅢ':
                Label = 39
            elif self.phonemes[i].label == 'ㅣ':
                Label = 40

            # mfcclist.append()
            writeRow = []
            for i in range(len(mfcclist)):
                for j in range(len(mfcclist[i])):
                    writeRow.append(mfcclist[i][j])
            writeRow.append(Label)

            writer.writerow(writeRow)
            