import math
import numpy as np
from collections import namedtuple
import python_speech_features as psf
import Framing
import heapq


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


def GetCenterOfMass(input, xy='xy'):
    '''
    input : 2차원 배열
    '''
    centerX = []
    centerY = []

    for i in range(len(input)):
        m = 0
        SumX = 0
        SumY = 0
        for j in range(len(input[i])):
            m += input[i][j]
            SumX += j*input[i][j]
            SumY += input[i][j]**2
        if not m == 0:
            centerX.append(SumX/m)
            centerY.append(SumY/(2*m))
        else:
            centerX.append(-1)
            centerY.append(-1)
    
    if xy=='xy':
        return centerX, centerY
    elif xy=='x':
        return centerX
    elif xy=='y':
        return centerY

def Get_TOP_X(Spec):
    ret = []
    for i in range(len(Spec)):
        Max = Spec[i][0]
        MaxIndex = 0
        for j in range(len(Spec[i])):
            if Max < Spec[i][j]:
                Max = Spec[i][j]
                MaxIndex = j
        ret.append(MaxIndex)
    return ret


def GetInclinations_abs(input):
    inclinations = []
    for i in range(len(input)-1):
        inclination = input[i+1]-input[i]
        inclinations.append(abs(inclination))
    return inclinations