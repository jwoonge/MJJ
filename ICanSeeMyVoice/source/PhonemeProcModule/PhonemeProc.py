import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import Framing
from collections import namedtuple
import Calculator as c
import python_speech_features as psf
import numpy as np
from scipy.ndimage import filters


class PhonemeProc():
  def __init__(self, sample_rate):
    self.sample_rate = sample_rate
    self.frame_size = int((self.sample_rate / 16000) * 512)
    self.interval = int((self.sample_rate / 16000) * 480)

  def getPhonemes(self, pcmValue):
    self.pcmValue = pcmValue

    self.Framing_pcm()

    self.Spec = c.Spectrogram(self.pcm_framed, self.sample_rate)
    self.Spec_g = filters.gaussian_filter(self.Spec, 3)

    self.Mark_Empty()
    self.Mark_UV()
    self.Check_Empty_UV()
    self.Check_Empty_AVG()
    self.UV_list = self.UV_Section()

    self.Separate()

    return self.Make_MFCC()

  def Check_Empty_AVG(self):
    self.frame_table[0].Empty = True
    self.frame_table[-1].Empty = True

    self.sect_start = []
    self.sect_end = []
    for i in range(len(self.frame_table)-1):
      if self.frame_table[i].Empty and not self.frame_table[i+1].Empty:
        self.sect_start.append(i+1)
      if not self.frame_table[i].Empty and self.frame_table[i+1].Empty:
        self.sect_end.append(i+1)

    if not (len(self.sect_start)==1 and len(self.sect_end)==1):
      self.avgSpec = []
      for i in range(len(self.frame_table)):
        sumSpec = 0
        for j in range(len(self.Spec[i])):
          sumSpec += self.Spec[i][j]
        sumSpec /= len(self.Spec[0])
        self.avgSpec.append(sumSpec)
      
      selected_sect = 0
      sect_value = -1
      for i in range(len(self.sect_start)):
        temp_sect = 0
        for j in range(self.sect_start[i],self.sect_end[i]):
          temp_sect += self.avgSpec[j]
        if temp_sect > sect_value:
          selected_sect = i
          sect_value = temp_sect
      
      for i in range(len(self.frame_table)):
        if not i in range(self.sect_start[selected_sect], self.sect_end[selected_sect]):
          self.frame_table[i].Empty = True
          self.frame_table[i].UV = 0
      
  def Separate(self):
    Graph = c.GetDistance(self.Spec_g, th=5)
    Graph_i = c.GetInclinations(Graph)

    self.phonemes = []
    ### phonemes : list of namedtuple('phoneme', [point, UV, pcm_start, pcm_end])
    for i in range(len(self.UV_list)):
      if self.UV_list[i].UV == 'U':
        # UV_list[i].start : end 에서 무조건 하나 가져옴
        point = self.GetPointFromRange(Graph, self.UV_list[i].start, self.UV_list[i].end)
        temp = namedtuple('phoneme', ['point', 'UV', 'pcm_start', 'pcm_end'])
        temp.point = point
        temp.UV = 'U'
        self.phonemes.append(temp)
      elif self.UV_list[i].UV == 'V':
        # graph for문 돌면서 0인 구간 중 가운뎃값 가져옴
        points = self.GetAllZeroPointFromRange(Graph, self.UV_list[i].start, self.UV_list[i].end)
        if points==[]:
          convexes = c.GetConvex_range(Graph_i, self.UV_list[i].start, self.UV_list[i].end)
          minindex = convexes[0]
          minvalue = Graph[convexes[0]]
          for j in range(len(convexes)):
            if minvalue > Graph[convexes[j]]:
              minvalue = Graph[convexes[j]]
              minindex = convexes[j]
            points.append(minindex)

        for j in range(len(points)):
          temp = namedtuple('phoneme', ['point', 'UV', 'pcm_start', 'pcm_end'])
          temp.point = points[j]
          temp.UV = 'V'
          self.phonemes.append(temp)

    ### PostTreat : calculate p_start, p_end
    for i in range(len(self.phonemes)):
      f_start = Framing.Index_frame_to_origin(self.phonemes[i].point, self.frame_size, self.interval)
      f_end = f_start + 2 * self.frame_size - self.interval
      f_range = (f_start - f_end)
      sectlen = int(0.05 * self.sample_rate)
      p_start = f_start - int((sectlen - f_range) / 2) + 650

      if p_start < 0:
        p_start = 0

      p_end = p_start + sectlen

      if p_end >= len(self.pcmValue):
        p_end = len(self.pcmValue) - 1
        p_start = p_end - sectlen
      self.phonemes[i].pcm_start = p_start
      self.phonemes[i].pcm_end = p_end

  def UV_Section(self):
    ret = []
    ret2 = []
    start = 0
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
          j += 1
          break
        j += 1
        # count+=1
      i = j

    i = 0
    while i < len(ret) - 1:
      if i == 0 and ret[i].UV == 0:
        i += 1
        continue
      if ret[i].UV == 0:
        ret[i - 1].end = ret[i + 1].end
        ret[i + 1].UV = 0
        i += 1
      i += 1

    for i in range(len(ret)):
      if ret[i].UV == 2:
        ret[i].UV = 'U'
      elif ret[i].UV == 3:
        ret[i].UV = 'V'

    for i in range(len(ret)):
      if ret[i].UV != 0:
        ret2.append(ret[i])

    return ret2

  def Mark_Empty(self):
    self.maxes = []
    for i in range(len(self.frame_table)):
      self.maxes.append(max(self.Spec[i]))
    OptMax = max(self.maxes)
    LEMax = max(self.frame_LE)
    for i in range(len(self.frame_table)):
      if max(self.Spec[i]) < OptMax / 100:
        self.frame_table[i].Empty = True
      if self.frame_LE[i] < 0.25 * LEMax:
        self.frame_table[i].Empty = True

  def Mark_UV(self):

    ### 50 이상인 것들이 12개 이상 있으면 유성음 ###
    th_max = 50
    for i in range(len(self.Spec)):
      count = 0
      for j in range(len(self.Spec[i])):
        if self.Spec[i][j] > th_max:
          count += 1
      if count > self.frame_size / 40:
        self.frame_table[i].UV = 3

    ### max가 1000 이상인 프레임은 유성음 ###
    for i in range(len(self.frame_table)):
      if self.maxes[i] > 1000:
        self.frame_table[i].UV = 3

  def Check_Empty_UV(self):
    ## Check UV line with time ##

    minVlen = int((0.10 * self.sample_rate - self.frame_size) / (self.frame_size - self.interval))
    start = 0
    end = start
    while (end < len(self.frame_table)):
      end = start
      if end < len(self.frame_table) and self.frame_table[end].UV == 3:
        while end < len(self.frame_table) - 1 and self.frame_table[end + 1].UV == 3:
          end += 1
      lenSect = end - start
      if lenSect < minVlen:
        for i in range(start, end + 1):
          if i < len(self.frame_table) and not self.frame_table[i].Empty:
            self.frame_table[i].UV = 2
      start = end + 1

    ## Check /b or noise by _U_
    points = []  # points : 무음->유음, 유음->무음 가는 지점들
    if not self.frame_table[0].Empty:
      points.append(0)
    for i in range(len(self.frame_table) - 1):
      if self.frame_table[i].Empty and not self.frame_table[i + 1].Empty:
        points.append(i + 1)
      elif not self.frame_table[i].Empty and self.frame_table[i + 1].Empty:
        points.append(i + 1)
    if not self.frame_table[-1].Empty:
      points.append(len(self.frame_table) - 1)

    for i in range(len(points) - 1):
      start = points[i]
      end = points[i + 1]
      countV = 0
      for j in range(start, end):
        if self.frame_table[j].UV == 3:
          countV += 1
      if countV == 0:  # not exist V sound in range(start,end)
        for j in range(start, end):
          self.frame_table[j].Empty = True
          self.frame_table[j].UV = 0
      i += 1

  def Framing_pcm(self):
    self.pcm_framed = Framing.Framing(self.pcmValue, self.frame_size, self.interval)
    self.frame_table = []
    for i in range(len(self.pcm_framed)):
      temp = namedtuple('Status', ['Empty', 'UV'])
      temp.Empty = False
      temp.UV = 0
      self.frame_table.append(temp)
    self.frame_LE = c.Log_Energy(self.pcm_framed)

  def GetPointFromRange(self, Graph, start, end):
    zero_flag = False
    for i in range(start, end):
      if Graph[i] == 0:
        zero_flag = True
        break

    if not zero_flag:
      min = Graph[start]
      minindex = start
      for i in range(start, end):
        if Graph[i] < min:
          min = Graph[i]
          minindex = i
      return minindex

    else:
      z_start = start
      z_end = end
      for i in range(start, end):
        if Graph[i] == 0:
          z_start = i
          z_end = i
          break
      for i in range(z_start, end - 1):
        if Graph[i + 1] == 0:
          z_end = i
        else:
          break
      return int((z_start + z_end) / 2)

  def GetAllZeroPointFromRange(self, Graph, start, end):
    ret_points = []
    z_start = start
    z_end = z_start
    while z_end < end:
      while z_start < end and Graph[z_start] != 0:
        z_start += 1
      z_end = z_start
      if z_end < end and Graph[z_end] == 0:
        while z_end < end-1 and Graph[z_end + 1] == 0:
          z_end += 1
      zero_point = int((z_start + z_end) / 2)
      if zero_point >= 0 and zero_point <len(Graph):
        if Graph[zero_point] == 0:
          ret_points.append(int((z_start + z_end) / 2))
      z_start = z_end + 1
      z_end = z_start
    return ret_points

  def Make_MFCC(self):
    retMFCC = []
    retUV = []
    for i in range(len(self.phonemes)):
      WriteList = self.pcmValue[self.phonemes[i].pcm_start: self.phonemes[i].pcm_end]
      mfcclist = []
      mfccWriteList = np.array(WriteList)
      temp = psf.mfcc(mfccWriteList, samplerate=self.sample_rate, winlen=0.01, winstep=0.01, nfft=self.frame_size,
                      numcep=12)
      for k in range(temp.shape[0]):
        templist = []
        for j in range(temp.shape[1]):
          templist.append(temp[k][j])
        mfcclist.append(templist)

      retUV.append(self.phonemes[i].UV)
      retMFCC.append(mfcclist)
    return retMFCC, retUV