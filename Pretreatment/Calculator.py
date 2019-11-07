import math
import numpy as np
from collections import namedtuple

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

def Normalize(input_Spectrogram):
    normalized_Spectrogram = []
    default_area = 100*len(input_Spectrogram[0])
    for i in range(len(Spectrogram)):
        normalized_fft = []
        area = 0
        for j in range(len(input_Spectrogram[i])):
            area+=input_Spectrogram[i][j]
        rate = area / default_area
        for j in range(len(input_Spectrogram[i])):
            normalized_fft.append(input_Spectrogram[i][j]*rate)
        normalized_Spectrogram.append(normalized_fft)
    return normalized_Spectrogram

def GetInclinations(input):
    inclinations = []
    for i in range(len(input)-1):
        inclination = input[i+1]-input[i]
        inclinations.append(inclination)
    return inclinations

def GetConvex(input, er = 5):
    inclinations = GetInclinations(input)

    points = []
    inflections = []
    for i in range(len(inclinations)-1):
        if inclinations[i]*inclinations[i+1]<=0:
            inflections.append(i)

    start = 0
    end = start

    while end<len(inflections)-1 :

        end = start
        while(end<len(inflections)-1) and abs(inflections[end+1]-inflections[end]<=er):
            end+=1
        pointIndex = start
        preStart = inflections[start]-1
        postEnd = inflections[end]+1
        Valid = True
        state = None
        if preStart < 0:
            preStart = 0
        if postEnd >= len(inclinations):
            postEnd = len(inclinations)-1

        if inclinations[preStart] >=0 and inclinations[postEnd]<0 :
            state = 'Concave'
            Max = input[start]
            for i in range(start, end+1):
                if(input[inflections[i]]>Max):
                    Max = input[inflections[i]]
                    pointIndex = i
        
        elif inclinations[preStart] < 0 and inclinations[postEnd]>=0 :
            state = 'Convex'
            Min = input[start]
            for i in range(start, end+1):
                if(input[inflections[i]]<Min):
                    Min = input[inflections[i]]
                    pointIndex = i
            if input[inflections[pointIndex]]<0.02:
                Valid = False
                #print("One point has been deleted by Under_value_Error")
        
        else :
            state = 'Stable'
            zero = inclinations[inflections[start]]
            for i in range(start, end+1):
                if(abs(inclinations[inflections[i]])<abs(zero)):
                    zero = inclinations[inflections[i]]
                    pointIndex = i
        
        if Valid:
            temp = namedtuple('Coordinate',['point','state'])
            temp.point = inflections[pointIndex]+1
            temp.state = state
            points.append(temp)
        start = end + 1

    return points



def GetDistance(input, weight=[1]):
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
            temp += (weight[j] * (input[i][j] - input[i+1][j])**2)**0.5
        ret.append(temp)

    return ret