from scipy.io.wavfile import write
import sounddevice as sd


def trainRECORDER():
    trainRECORDER.count += 1
    count_s = str(trainRECORDER.count)
    formatname = '.wav'
    filename = 'train' + count_s + formatname
    fs = 16000  # Sample rate
    seconds = 3  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, myrecording)  # Save as WAV file

def testRECORDER():
    testRECORDER.count += 1
    count_s = str(testRECORDER.count)
    formatname = '.wav'
    filename = 'test' + count_s + formatname
    fs = 16000  # Sample rate
    seconds = 5  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, myrecording)  # Save as WAV file


trainRECORDER.count = 0
testRECORDER.count = 0
