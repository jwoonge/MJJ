import numpy as np
import math

class PCMdata():
    def __init__(self,_value, _samplerate=16000):
        self.value = _value
        self.value_count = len(self.value)
        self.Fs = _samplerate