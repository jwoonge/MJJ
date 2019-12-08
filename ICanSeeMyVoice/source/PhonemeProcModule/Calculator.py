import math
import numpy as np
from collections import namedtuple


def pickBestN(input_list, N, xy='x'):
    temp = []
    for i in range(len(input_list)):
        t = namedtuple("Coordinate", ['value', 'index'])
        t.value = input_list[i]
        t.index = i
        temp.append(t)
    temp = sorted(temp, key=lambda x:x.value,reverse=True)
    ret = []
    if N <= len(temp):
        if xy=='x':
            for i in range(N):
                ret.append(temp[i].index)
        elif xy=='y':
            for i in range(N):
                ret.append(temp[i].value)

    return ret

def Log_Energy(input_frames):
    LogEnergy = []
    for i in range(len(input_frames)):
        sum = 0
        for j in range(len(input_frames[0])):
            sum += input_frames[i][j]*input_frames[i][j]
        tmp = max([math.e, sum])
        LogEnergy.append(math.log(tmp))
    minE = min(LogEnergy)
    for i in range(len(input_frames)):
        LogEnergy[i] -= minE
    return LogEnergy

def Spectrogram(input_frames, sample_rate):
    Spec = []
    frame_size = len(input_frames[0])
    for i in range(len(input_frames)):
        tempFFT = FFT(input_frames[i], sample_rate, frame_size)
        Spec.append(tempFFT)
    return Spec

def FFT(input_frame, sample_rate, frame_size):
    NFFT = frame_size
    Y = np.fft.fft(input_frame)/NFFT
    Y = Y[range(math.trunc(NFFT/4))]
    fft = 2*abs(Y)
    return fft

def GetInclinations(input):
    inclinations = []
    for i in range(len(input)-1):
        inclination = input[i+1]-input[i]
        inclinations.append(inclination)
    return inclinations

def GetConvex_range(input_inclination, start, end):
    convex = []
    for i in range(start+1, end):
        if(input_inclination[i-1] < 0 and input_inclination[i] > 0):
            convex.append(i)
    return convex

def GetDistance(input, th, weight=[1]):
    '''
    input : 2-dim list
    weight : 1-dim list, length = len(input), default=[1,]
    '''
    if weight == [1] :
        for i in range(len(input[0])-1):
            weight.append(1)

    ret = []
    for i in range(len(input)-1):
        temp = 0
        for j in range(len(input[0])):
            differ = abs(input[i][j] - input[i+1][j])
            if differ<th:
                differ = 0
            temp += weight[j] * (differ**2)
        ret.append(temp)

    return ret