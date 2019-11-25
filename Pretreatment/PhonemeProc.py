from PCMdata import PCMdata
import RWwav
import Framing
from collections import namedtuple
import Calculator as c
import SoundVisualization as sv
from StandardPro import standard
import sys
import python_speech_features as psf
import numpy as np
import pandas as pd
import math
from scipy.ndimage import filters

class PhonemeProc():
    def __init__(self):
        self.StandardProc=standard()


    def DoProcess(self, fileNo=0, fileDir="Default", pcmwav="pcm", debug=True, separate=False, Graph=False):
        self.Settings(fileNo, fileDir, pcmwav, debug, separate)
        if not self.file_valid:
            return False

        self.Spec = c.Spectrogram(self.pcm_framed, self.pcm.Fs)
        self.Spec_blur = c.Blurring(self.Spec, self.mask)
        self.Mark_Empty()
        self.Mark_UV()
        self.Check_Empty_UV()
        self.UV_list = self.UV_Section()
        self.g = filters.gaussian_filter1d(c.GetInclinations_abs(filters.gaussian_filter1d(self.frame_LE,0.1)),2.5)
        self.g_inc = c.GetInclinations(self.g)
        self.Separate()
        if Graph:
            self.Show_Graph()
        if debug:
            self.Separating_write('Separated')
            for i in range(len(self.phonemes)):
                print(self.phonemes[i].point," ", self.phonemes[i].label)
        '''
        if separate:
            self.Make_dataset()
        '''

        return True

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
                    if not temp.label=='S':
                        self.phonemes.append(temp)

        ### Case 2 : Number of Phonemes from whole sector is matched with Expected ###


        ### Case 3 : worst case - Timing matching
        
        ### PostTreat : calculate p_start, p_end
        for i in range(len(self.phonemes)):
            f_start = Framing.Index_frame_to_origin(self.phonemes[i].point,self.frame_size,self.interval)
            f_end = f_start + 2 * self.frame_size - self.interval
            f_range = (f_start-f_end)
            sectlen = int(0.05*self.pcm.Fs)
            #p_start = f_start - int((sectlen-f_range)/2)
            #p_end = p_start + sectlen
            p_start = f_start - int((sectlen-f_range)/2) + 650
            p_end = p_start + sectlen
            self.phonemes[i].pcm_start = p_start
            self.phonemes[i].pcm_end = p_end


    def Get_Points_from_Sector(self, start, end, n, UV):
        ### from the sector in range(start, end), return N points as list of integer ###
        points = []
        
        if UV=='V':
            every_convex = c.GetConvex_range(self.g_inc,start,end)
            convexes = []
            for i in range(len(every_convex)):
                temp = namedtuple('ssibal',['x','y'])
                temp.x = every_convex[i]
                temp.y=self.g[every_convex[i]]
                convexes.append(temp)
            
            convexes = sorted(convexes, key=lambda x:x.y)
            for i in range(n):
                points.append(convexes[i].x)
            

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

        if self.debug:
            print("detected UV")
            for i in range(len(ret2)):
                print("   start:",ret2[i].start, ' end:', ret2[i].end, ' UV:', ret2[i].UV)

        return ret2

    def Mark_Empty(self, blur=False):
        if blur:
            Spect = self.Spec_blur
        else:
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

    def Mark_UV(self, blur=False):
        if blur:
            Spect = self.Spec_blur
        else:
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
        
        minVlen = int((0.05 * self.pcm.Fs - self.frame_size) / (self.frame_size - self.interval))
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

    def Settings(self, fileNo, fileDir, pcmwav, debug, separate):
        self.separate = separate
        self.debug=debug
        if fileNo ==0:
            self.fileNo=1
        else:
            self.fileNo=fileNo
        self.Hit=False
        if fileDir=="Default":
            Directory=self.Directory_Make(fileNo)
        else:
            Directory=fileDir
        self.StandardProc.fileread(Directory)
        self.Pronun=self.StandardProc.getPronunciation()
        self.UV_txt = self.StandardProc.getIsVoiced()

        self.file_valid = self.StandardProc.getFileValid()

        self.pcm=RWwav.Read_file(Directory+'.'+pcmwav)
        if self.debug:
            print("sampleRate : ", self.pcm.Fs)
        self.frame_size=int((self.pcm.Fs / 16000) * 512)
        self.interval=int((self.pcm.Fs / 16000) * 480)
        if self.debug:
            direc="Output/origin" + str(fileNo) + ".wav"
            RWwav.Write_wav(direc, self.pcm.value, self.pcm.Fs)

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
        self.pcm_framed=Framing.Framing(self.pcm.value, self.frame_size, self.interval)
        self.frame_table=[]
        for i in range(len(self.pcm_framed)):
            temp=namedtuple('Status', ['Empty', 'UV'])
            temp.Empty=False
            temp.UV=0
            self.frame_table.append(temp)
        self.frame_LE=c.Log_Energy(self.pcm_framed)
        
    def Directory_Make(self, fileNo=0, filename_first='input/KsponSpeech_'):
        filename_second=''

        if fileNo < 10:
	        filename_second='00000' + str(fileNo)
        elif fileNo < 100:
            filename_second='0000' + str(fileNo)
        elif fileNo < 1000:
            filename_second='000' + str(fileNo)
        elif fileNo < 10000:
            filename_second='00' + str(fileNo)
        elif fileNo < 100000:
            filename_second='0' + str(fileNo)
        else:
            filename_second=str(fileNo)
        filename=filename_first + filename_second

        return filename

    def Show_Graph(self):
        bounds=[]
        for i in range(len(self.frame_table)-1):
            if self.frame_table[i].Empty ^ self.frame_table[i+1].Empty:
                bounds.append(i)

        UVline = []
        for i in range(len(self.frame_table)-1):
            if self.frame_table[i].UV ^ self.frame_table[i+1].UV:
                UVline.append(i)

        temptoShow=[]
        for i in range(len(self.frame_table)):
            temptoShow.append(self.frame_table[i].UV)

        centerX, centerY = c.GetCenterOfMass(self.Spec)

        centerX_pcm, centerY_pcm = c.GetCenterOfMass(self.pcm_framed)
        sv.Show_Array(centerX_pcm, title="centerX_pcm", input_list_r=bounds, input_list_c=UVline)
        sv.Show_Array(centerY_pcm, title="centerY_pcm", input_list_r=bounds, input_list_c=UVline)

        sv.Show_Array(c.GetDistance(c.Normalize(self.Spec_blur)), input_list_r=bounds, input_list_c=UVline, title="normalized distance")
        sv.Show_Array(c.GetDistance(c.Normalize_max(self.Spec_blur)), title="normalized_max distance", input_list_r=bounds, input_list_c=UVline)
        sv.Show_Array(c.GetDistance(c.Normalize_th(self.Spec_blur)), title="normalized_th distance", input_list_r=bounds, input_list_c=UVline)
        #sv.Show_Array(c.GetDistance(c.Normalize_max_th(self.Spec_blur)), title="normalized_max_th distance", input_list_r=bounds, input_list_c=UVline)
        sv.Show_Array(c.GetZeroCrossOver(Framing.Framing(c.Variation(self.frame_LE,7),32,30)),title="ssssssssss!!")
        #sv.Show_Array(c.GetZeroCrossOver(Framing.Framing(c.GetInclinations(c.GetInclinations(self.frame_LE)),32,30),0),title="incli_d_0 Crossover")
        #sv.Show_Array(c.GetZeroCrossOver(Framing.Framing(c.GetInclinations(c.GetInclinations(self.frame_LE)),32,30),0.1),title="incli_d_0.1 Crossover")
        #sv.Show_Array(c.GetZeroCrossOver(Framing.Framing(c.GetInclinations(c.GetInclinations(self.frame_LE)),32,30),0.2),title="incli_d_0.2 Crossover")
        sv.Show_Spectrogram(self.Spec, vmin=0, vmax=250,input_list_r=bounds, input_list_c=UVline)
        sv.Show_Array(temptoShow, title="UV", input_list_c=UVline, input_list_r = bounds)

        maxpcm = []
        for i in range(len(self.pcm_framed)):
            maxpcm.append(max(self.pcm_framed[i]))

        sv.Show_Array(c.Sum_PCM(self.pcm_framed),title="SumPCM",input_list_r=bounds,input_list_c=UVline)
        sv.Show_Array(c.Sum_PCM(Framing.Framing(self.pcm.value, frame_size=32, interval=0)),title="SumPCM-32-0")
        sv.Show_Array(c.Sum_PCM(Framing.Framing(self.pcm.value, frame_size=32, interval=2)),title="SumPCM-32-2")
        sv.Show_Array(c.Sum_PCM(Framing.Framing(self.pcm.value, frame_size=64, interval=0)),title="SumPCM-64-0")
        sv.Show_Array(c.Sum_PCM(Framing.Framing(self.pcm.value, frame_size=64, interval=2)),title="SumPCM-64-2")
        '''
        sv.Show_Array(c.GetZeroCrossOver(self.pcm_framed,max(maxpcm)/300),title="CrossOver-/300",input_list_r=bounds,input_list_c=UVline)
        sv.Show_Array(c.GetZeroCrossOver(self.pcm_framed,300),title="CrossOver-300",input_list_r=bounds,input_list_c=UVline)
        sv.Show_Array(c.GetZeroCrossOver(self.pcm_framed,200),title="CrossOver-200",input_list_r=bounds,input_list_c=UVline)
        sv.Show_Array(c.GetZeroCrossOver(self.pcm_framed,100),title="CrossOver-100",input_list_r=bounds,input_list_c=UVline)
        '''

        sv.Show_Array(self.frame_LE, title="Log Energy", input_list_c=UVline, input_list_r=bounds)
        sv.Show_Array(centerX, title="center_X", input_list_c=UVline, input_list_r=bounds)
        sv.Show_Array(centerY, title="center_Y", input_list_c=UVline, input_list_r=bounds)
        sv.Show_Array(c.Get_TOP_Y(self.Spec), title="TOP_Y", input_list_c  =UVline, input_list_r=bounds)
        sv.Show_Array(c.Distribution(self.Spec), title="distribution", input_list_c=UVline, input_list_r=bounds)
        sv.Show_Array(c.GetQuartile(self.Spec), title="quartile", input_list_c=UVline, input_list_r=bounds)
        sv.Show_Array(c.getArea(self.Spec), title="Area", input_list_c  =UVline, input_list_r=bounds)



    def Separating_write(self, fileDir):
        RWwav.removeAllFile(fileDir)
        number=1
        for i in range(len(self.phonemes)):
            directory = fileDir + '/' + str(number) + '.wav'
            number += 1
            WriteList = self.pcm.value[self.phonemes[i].pcm_start : self.phonemes[i].pcm_end]
            RWwav.Write_wav(directory, WriteList, self.pcm.Fs)



'''
    def Make_dataset(self):
        print("Make dataset...")
        cutting_sec = 0.05
        cutting_range = int(cutting_sec * self.pcm.Fs)
        number = 1
        for i in range(len(self.frame_table)):
            if self.frame_table[i].Hit:
                number += 1
                WriteList = []
                mid = Framing.Index_frame_to_origin(i, self.frame_size, self.interval) + int((self.frame_size) / 2)
                if (mid - int(cutting_range * 0.5) > 0) and (mid + int(cutting_range * 0.5) - 1 < self.pcm.value_count):
                    for j in range(cutting_range):
                        if mid - int(cutting_range * 0.5) + j < self.pcm.value_count:
                            WriteList.append(self.pcm.value[mid - int(cutting_range * 0.5) + j])
                        else:
                            print('Index out of range in Separating_Write')
                  ###
                Label =1 #self.Pronun[number-2]
                mfcclist = []
                mfccWriteList = np.array(WriteList)
                temp = psf.mfcc(mfccWriteList, samplerate=self.pcm.Fs, winlen=0.01, nfft=self.frame_size, numcep=12)
                print(temp.shape)
                for i in range(temp.shape[0]):
                    templist = []
                    for j in range(temp.shape[1]):
                        templist.append(temp[i][j])
                    mfcclist.append(templist)
                if self.Pronun == 'ㄱ':
                    Label = 1
                elif self.Pronun == 'ㄴ':
                    Label = 2
                elif self.Pronun == 'ㄷ':
                    Label = 3
                elif self.Pronun == 'ㄹ':
                    Label = 4
                elif self.Pronun == 'ㅁ':
                    Label = 5
                elif self.Pronun == 'ㅂ':
                    Label = 6
                elif self.Pronun == 'ㅅ':
                    Label = 7
                elif self.Pronun == 'ㅇ':
                    Label = 8
                elif self.Pronun == 'ㅈ':
                    Label = 9
                elif self.Pronun == 'ㅊ':
                    Label = 10
                elif self.Pronun == 'ㅋ':
                    Label = 11
                elif self.Pronun == 'ㅌ':
                    Label = 12
                elif self.Pronun == 'ㅍ':
                    Label = 13
                elif self.Pronun == 'ㅎ':
                    Label = 14
                elif self.Pronun == 'ㄲ':
                    Label = 15
                elif self.Pronun == 'ㄸ':
                    Label = 16
                elif self.Pronun == 'ㅃ':
                    Label = 17
                elif self.Pronun == 'ㅆ':
                    Label = 18
                elif self.Pronun == 'ㅉ':
                    Label = 19
                elif self.Pronun == 'ㅏ':
                    Label = 20
                elif self.Pronun == 'ㅐ':
                    Label = 21
                elif self.Pronun == 'ㅑ':
                    Label = 22
                elif self.Pronun == 'ㅒ':
                    Label = 23
                elif self.Pronun == 'ㅓ':
                    Label = 24
                elif self.Pronun == 'ㅔ':
                    Label = 25
                elif self.Pronun == 'ㅕ':
                    Label = 26
                elif self.Pronun == 'ㅖ':
                    Label = 27
                elif self.Pronun == 'ㅗ':
                    Label = 28
                elif self.Pronun == 'ㅘ':
                    Label = 29
                elif self.Pronun == 'ㅙ':
                    Label = 30
                elif self.Pronun == 'ㅚ':
                    Label = 31
                elif self.Pronun == 'ㅛ':
                    Label = 32
                elif self.Pronun == 'ㅜ':
                    Label = 33
                elif self.Pronun == 'ㅝ':
                    Label = 34
                elif self.Pronun == 'ㅞ':
                    Label = 35
                elif self.Pronun == 'ㅟ':
                    Label = 36
                elif self.Pronun == 'ㅠ':
                    Label = 37
                elif self.Pronun == 'ㅡ':
                    Label = 38
                elif self.Pronun == 'ㅢ':
                    Label = 39
                elif self.Pronun == 'ㅣ':
                    Label = 40

                # mfcclist.append()
                mfcclist.append(Label)
                DataFrame = pd.DataFrame(data=[mfcclist])
                DataFrame.to_csv("MFCC.csv", mode='a', header=None)

                '''