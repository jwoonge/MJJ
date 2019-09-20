from Sound import Sound
import numpy

import python_speech_features as psf

test1 = Sound("KsponSpeech_000001.pcm")
test1.PrintHeader()
sample_rate = test1.Header.FMT.SampleRate
#emphasized_signal = test1.getValue()

testmfcc = psf.mfcc(test1.getValue())

print(testmfcc)
print(len(testmfcc))
print(testmfcc.shape)