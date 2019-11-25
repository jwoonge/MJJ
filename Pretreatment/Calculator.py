import math
import numpy as np
from collections import namedtuple
import python_speech_features as psf
import Framing
import heapq

def getMFCC(input):
    mfcc = psf.mfcc(np.array(input),winlen=512/16000,winstep=480/16000)
    return mfcc

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
    '''
    for i in range(len(input_Spectrogram)):
        for j in range(len(input_Spectrogram[i])):
            if input_Spectrogram[i][j]<10:
                input_Spectrogram[i][j]=0
    '''

    normalized_Spectrogram = []
    default_area = 100*len(input_Spectrogram[0])
    for i in range(len(input_Spectrogram)):
        normalized_fft = []
        area = 0
        for j in range(len(input_Spectrogram[i])):
            area+=input_Spectrogram[i][j]
        if not area == 0:
            rate = default_area / area
        else:
            rate = -1
            #print("Divided by zero Error!")
        for j in range(len(input_Spectrogram[i])):
            normalized_fft.append(input_Spectrogram[i][j]*rate)
        normalized_Spectrogram.append(normalized_fft)
    return normalized_Spectrogram

def getArea(input_Spec):
    ret = []
    for i in range(len(input_Spec)):
        Area = 0
        for j in range(len(input_Spec[i])):
            Area+=input_Spec[i][j]
        if Area==0:
            Area=-1
        ret.append(Area)
    return ret

def Standard_Deriv(input_Spec):
    Standard_Derivs = []
    for i in range(len(input_Spec)):
        Sum = 0
        Deriv = 0
        for j in range(len(input_Spec[i])):
            Sum += input_Spec[i][j]
        Avg = Sum / len(input_Spec[i])
        for j in range(len(input_Spec[i])):
            Dist = abs(input_Spec[i][j]-Avg)
            if Dist< 20:
                Dist = 0
            else:
                Dist = Dist-20
            Deriv+=(Dist)**2
        Standard_Derivs.append(Deriv**0.5)
    return Standard_Derivs

def GetInclinations(input):
    inclinations = []
    for i in range(len(input)-1):
        inclination = input[i+1]-input[i]
        inclinations.append(inclination)
    return inclinations

def GetConvex(input):
    inclinations = GetInclinations(input)
    convex = []
    for i in range(1, len(inclinations)):
        if(inclinations[i-1] < 0 and inclinations[i] > 0):
            convex.append(i)
    return convex

def GetConvex_range(input_inclination, start, end):
    convex = []
    for i in range(start+1, end):
        if(input_inclination[i-1] < 0 and input_inclination[i] > 0):
            convex.append(i)
    return convex
    
def GetConcave(input):
    inclinations = GetInclinations(input)
    concave = []
    for i in range(1, len(inclinations)):
        if(inclinations[i-1] > 0 and inclinations[i] < 0):
            concave.append(i)
    return concave

def GetInflection(input, er=5):
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
            Max = input[inflections[start]]
            for i in range(start, end+1):
                if(input[inflections[i]]>Max):
                    Max = input[inflections[i]]
                    pointIndex = i
        
        elif inclinations[preStart] < 0 and inclinations[postEnd]>=0 :
            state = 'Convex'
            Min = input[inflections[start]]
            for i in range(start, end+1):
                if(input[inflections[i]]<Min):
                    Min = input[inflections[i]]
                    pointIndex = i
        
        else :
            state = 'Stable'
            '''
            zero = inclinations[inflections[start]]
            for i in range(start, end+1):
                if(abs(inclinations[inflections[i]])<abs(zero)):
                    zero = inclinations[inflections[i]]
                    pointIndex = i
                    '''
            Min = input[inflections[start]]
            for i in range(start, end+1):
                if(input[inflections[i]]<Min):
                    Min = input[inflections[i]]
                    pointIndex = i
        
        if Valid:
            temp = namedtuple('Coordinate',['point','state'])
            temp.point = inflections[pointIndex]+1
            temp.state = state
            points.append(temp)
        start = end + 1

    return points



def GetPhonmes(input, th_v, th_c):
    convex = GetConvex(input)
    concave = GetConcave(input)

    Cmap = ['None' for x in range(len(input))]
    convex_th = []
    concave_th = []

    for i in range(0, len(convex)):
        if(input[convex[i]] <= th_v):
            convex_th.append(convex[i])
    for i in range(len(concave)):
        if(input[concave[i]] > th_c):
            concave_th.append(concave[i])
    for i in range(len(concave_th)):
        Cmap[concave_th[i]] = 'Concave'
    for i in range(len(convex_th)):
        Cmap[convex_th[i]] = 'Convex'
    
    ret = []
    start = 0
    end = start
    while(end+1 < len(Cmap)):
        end = start
        lastConvex = -1
        firstConvex = -1
        count = 0
        while(end+1 < len(Cmap)) and not Cmap[end+1]=='Concave':
            end+=1
            if Cmap[end]=='Convex':
                count+=1
                if count==1:
                    firstConvex = end
                else:
                    lastConvex = end
        if count==1:
            ret.append(firstConvex)
        elif count>1:
            ret.append(int((firstConvex+lastConvex)/2))
        start = end+1

    return ret
    



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
            temp += (weight[j] * (input[i][j] - input[i+1][j])**2)
        ret.append(temp)

    return ret

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

def GetDist_COM(input):
    centerX, centerY = GetCenterOfMass(input)

    distance = []
    for i in range(len(input)-1):
        temp = ((centerX[i+1]-centerX[i])**2 + (centerY[i+1]-centerY[i])**2)**(0.5)
        distance.append(temp)

    return distance



def Blurring(input, mask):
    mask_sum = 0
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            mask_sum += 1

    spec = []
    for i in range(int(len(mask)/2)):
        tempspec_zero = [0 for x in range(int(len(mask[0])/2), len(input[0]) - int(len(mask[0])/2))]
        spec.append(tempspec_zero)
    for i in range (int(len(mask)/2), len(input) - int(len(mask)/2)):
        tempspec = []
        for j in range(int(len(mask[0])/2), len(input[0]) - int(len(mask[0])/2)):
            temp = 0
            for k in range((-1)*int(len(mask)/2), int(len(mask)/2)):
                for l in range((-1)*int(len(mask[0])/2), int(len(mask[0])/2)):
                    temp += input[i + k][j + l] * mask[k + int(len(mask) / 2)][l + int(len(mask[0]) / 2)]
            tempspec.append(temp/mask_sum)
        spec.append(tempspec)
    for i in range(int(len(mask)/2)):
        tempspec_zero = [0 for x in range(int(len(mask[0])/2), len(input[0]) - int(len(mask[0])/2))]
        spec.append(tempspec_zero)
    return spec

def SpecNumCheck(input_spec):
    resized_spec = []
    max = 0
    for i in range(0, len(input_spec)):
        for j in range(0, len(input_spec[i])):
            if (input_spec[i][j] > max):
                max = input_spec[i][j]

    resize_rate = 500 / max

    for i in range(0, len(input_spec)):
        temp = []
        for j in range(0, len(input_spec[i])):
            temp.append(input_spec[i][j] * resize_rate)
        resized_spec.append(temp)



    SpecNum = []
    Maps = []
    for i in range(len(resized_spec)):
        Map = []
        for j in range(len(resized_spec[i])):
            numofval = [0 for i in range(500)]
            for k in range(0, int(resized_spec[i][j])):
               numofval[k] = 1
            Map.append(numofval)
        Maps.append(Map)

    print(np.shape(Maps))
    # 1065 128 500
    for i in range(len(Maps)):
        onecountforvalue = []
        for j in range(500):
            count = 0
            for k in range(len(Maps[0])):
                if Maps[i][k][j]==1:
                    count += 1
            onecountforvalue.append(count)
        SpecNum.append(onecountforvalue)


    return SpecNum

def SpecChangeCheck(input_spec):
    resized_spec = []
    max = 0
    for i in range(0, len(input_spec)):
        for j in range(0, len(input_spec[i])):
            if (input_spec[i][j] > max):
                max = input_spec[i][j]

    resize_rate = 500 / max

    for i in range(0, len(input_spec)):
        temp = []
        for j in range(0, len(input_spec[i])):
            temp.append(input_spec[i][j] * resize_rate)
        resized_spec.append(temp)



    SpecNum = []
    Maps = []
    for i in range(len(resized_spec)):
        Map = []
        for j in range(len(resized_spec[i])):
            numofval = [0 for i in range(500)]
            for k in range(0, int(resized_spec[i][j])):
               numofval[k] = 1
            Map.append(numofval)
        Maps.append(Map)

    print(np.shape(Maps))
    # 1065 128 500
    for i in range(len(Maps)):
        onecountforvalue = []
        for j in range(500):
            count = 0
            for k in range(len(Maps[0])-1):
                if Maps[i][k][j] != Maps[i][k+1][j]:
                    count += 1
            onecountforvalue.append(count)
        SpecNum.append(onecountforvalue)


    return SpecNum
def Distribution_divby_Area(input_spec):
    distribution = Distribution(input_spec)
    area = getArea(input_spec)
    ret = []
    for i in range(len(input_spec)):
        ret.append(distribution[i]/area[i])
    return ret

def Distribution(input_spec):
    ret = []
    centerX, centerY = GetCenterOfMass(input_spec)
    for i in range(len(input_spec)):
        distribution = 0
        x = centerX[i]
        y = centerY[i]
        for j in range(len(input_spec[i])):
            distribution += input_spec[i][j]* abs(x-j)
        ret.append(distribution)
    return ret

def Distribution_Nabs(input_spec):
    ret = []
    centerX, centerY = GetCenterOfMass(input_spec)
    for i in range(len(input_spec)):
        distribution = 0
        x = centerX[i]
        y = centerY[i]
        for j in range(len(input_spec[i])):
            distribution += input_spec[i][j]* (x-j)
        ret.append(distribution)
    return ret

def get_Inc_Dist_Nabs(input_spec):
    Incs = []
    Dist = Distribution_Nabs(input_spec)
    for i in range(len(Dist)-1):
        Incs.append(Dist[i]-Dist[i+1])
    for i in range(len(Incs)):
        Incs[i] *= 100000*10000000
    framed_Incs = Framing.Framing(Incs,8,7)
    ret = Log_Energy(framed_Incs)
    print(framed_Incs)
    return ret



def GetQuartile(input_Spec):
    ret = []

    areas = getArea(input_Spec)
    for i in range(len(input_Spec)):
        Qarea = 0
        Qindex = 0
        while(Qarea < areas[i]/4):
            Qarea += input_Spec[i][Qindex]
            Qindex += 1
        Q1 = Qindex

        Qarea = 0
        Qindex = len(input_Spec[i])-1
        while(Qarea < areas[i]/4):
            Qarea += input_Spec[i][Qindex]
            Qindex -= 1
        Q3 = Qindex

        ret.append(Q3 - Q1)
    return ret

            
def GetZeroCrossOver(framed_pcm, th=0):
    ZeroCrossOver = []
    for i in range(len(framed_pcm)):
        count = 0
        for j in range(len(framed_pcm[0])-1):
            if (framed_pcm[i][j]-th) * (framed_pcm[i][j+1]-th) < 0:
                count += 1
            if (framed_pcm[i][j]+th) * (framed_pcm[i][j+1]+th) < 0:
                count += 1
        ZeroCrossOver.append(count)
    return ZeroCrossOver

def Get_TOP_Y(Spec):
    ret = []
    for i in range(len(Spec)):
        ret.append(max(Spec[i]))
    return ret

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

def Variation(input, maskN=7):
    ret = []
    input_blur = Blurring_1dim(input,maskN)
    for i in range(len(input)):
        ret.append(input_blur[i]-input[i])
    return ret

def Blurring_1dim(list, maskN):
    ret = []
    listN = len(list)
    maskRange = int(maskN/2) #5일때 2
    for i in range(maskRange): #5일때 2개 집어넣음
        ret.append(list[i])
    for i in range(maskRange, listN-maskRange):  # 300개면 2,298 범위
        temp = 0
        for j in range(-int(maskN/2),int(maskN/2)+1): # -2~+3
            temp += list[i+j]
        temp /= maskN
        ret.append(temp)
    for i in range(maskRange):
        ret.append(list[listN-maskRange+i])
    return ret
'''
def Blurring_1dim_mask(list, mask):
    ret = []
    listN = len(list)
    maskN = len(mask)
    maskRange = int(maskN/2)
    for i in range(maskRange, listN-maskRange):
        temp = 0
        for j in range(maskN):
            temp += list[i-maskRange]
'''

def Sum_PCM(input):
    SumPCM = []
    for i in range(len(input)):
        SumPCM.append(sum(input[i]))
    return SumPCM


def Normalize_max(input):
    TopY = Get_TOP_Y(input)
    MaxY = max(TopY)

    ret = []
    for i in range(len(input)):
        temp = []
        if MaxY == 0:
            rate = -100000
        else:
            rate = max(input[i]) / MaxY
        for j in range(len(input[i])):
            Normalized_value = input[i][j] / rate / 10000
            temp.append(Normalized_value)
        ret.append(temp)
    return ret

def Normalize_th(input, th=10):
    minus = input
    for i in range(len(input)):
        for j in range(len(input[i])):
            if minus[i][j] > th:
                minus[i][j] -= th
            else:
                minus[i][j] = 0
    
    return Normalize(minus)

def Normalize_max_th(input, th=10):
    minus = input
    for i in range(len(input)):
        for j in range(len(input[i])):
            if minus[i][j] >th:
                minus[i][j] -= th
            else:
                minus[i][j] = 0
    
    return Normalize_max(minus)

def GetInclinations_abs(input):
    inclinations = []
    for i in range(len(input)-1):
        inclination = input[i+1]-input[i]
        inclinations.append(abs(inclination))
    return inclinations