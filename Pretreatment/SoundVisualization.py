import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def Show_Spectrogram(input_Spec, vmin=0, vmax=150, input_list_c = [], input_list_r = []):
    ''' input : Spectogram [] '''
    plt.figure(figsize=(35,3))
    ax = sns.heatmap(np.transpose(input_Spec), vmin=vmin,vmax=vmax,cmap=sns.cm.rocket)
    ax.invert_yaxis()
    maxValue = len(input_Spec[0])
    minValue = 0
    for i in range(len(input_list_c)):
        plt.plot([input_list_c[i],input_list_c[i]],[minValue,maxValue],'c')
    for i in range(len(input_list_r)):
        plt.plot([input_list_r[i],input_list_r[i]],[minValue,maxValue],'r')

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

def Show_Array(input_array, title = "figure", input_list_c = [], input_list_r = []):
    input_array_t = []
    for i in range(len(input_array)-10):
        input_array_t.append(input_array[i+5])
    maxValue = max(input_array_t)
    minValue = min(input_array_t)
    x = np.arange(0,len(input_array),1)
    plt.figure(num=1,dpi=100,facecolor='white',figsize=(30,3))
    plt.title(title)
    for i in range(len(input_list_c)):
        plt.plot([input_list_c[i],input_list_c[i]],[minValue,maxValue],'c')
    for i in range(len(input_list_r)):
        plt.plot([input_list_r[i],input_list_r[i]],[minValue,maxValue],'r')
    plt.plot(x,input_array,'k')
    plt.plot([0,len(input_array)],[0,0])
    plt.xlim(0,len(input_array))
    plt.ylim(minValue,maxValue)
    plt.xlabel('frame')
    plt.ylabel('value')
    plt.show()
