import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def Show_Spectrogram(input_Spec):
    ''' input : Spectogram [] '''
    ax = sns.heatmap(np.transpose(input_Spec), vmin=150,vmax=400,cmap=sns.cm.rocket)
    ax.invert_yaxis()
    plt.show()

def Show_2dim_Array(input):
    _min = input[0][0]
    _max = input[0][0]
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] > _max:
                _max = input[i][j]
            if input[i][j] < _min:
                _min = input[i][j]

    ax = sns.heatmap(np.transpose(input), vmin = _min, vmax = _max, cmap = sns.cm.rocket)
    ax.invert_yaxis()
    plt.show()

def Show_Soundwave(input_array, samplerate=16000):
    '''input : array data'''
    Fs = samplerate
    T = 1/Fs
    te = len(input_array) / Fs
    t = np.arange(0,te,T)

    plt.figure(num=1, dpi=100, facecolor = 'white')
    plt.plot(t,input_array,'r')
    plt.xlim(0,te)
    plt.ylim(-32768,32767)
    plt.xlabel('time($sec$)')
    plt.ylabel('Soundwave')
    plt.show()

def Show_Array(input_array):
    maxValue = max(input_array)
    minValue = min(input_array)
    x = np.arange(0,len(input_array),1)
    plt.figure(num=1,dpi=100,facecolor='white')
    plt.plot(x,input_array,'r')
    plt.plot([0,len(input_array)],[0,0])
    plt.xlim(0,len(input_array))
    plt.ylim(minValue,maxValue)
    plt.xlabel('frame')
    plt.ylabel('value')
    plt.show()

