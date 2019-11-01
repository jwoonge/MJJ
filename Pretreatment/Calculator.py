import math
import numpy as np

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