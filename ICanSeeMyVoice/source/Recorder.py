import pyaudio
from source import SoundHandler
import numpy as np
'''
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)

# create pyaudio stream
stream = self.p.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)'''
import os
import wave
class recorder() :
  def __init__(self):
    self.value = []
    self.frames = []
    self.p = pyaudio.PyAudio()

    self.CHUNK = 2
    self.FORMAT = pyaudio.paInt16
    self.CHANNELS = 1
    self.RATE = 16000
    self.RECORD_SECONDS = 5
    self.recsignal = True

    self.stream = self.p.open(format=self.FORMAT, rate=self.RATE,channels=self.CHANNELS,
                               input_device_index=1, input=True,
                               frames_per_buffer=4096)



  def removeAllFile(self, filePath):
    if os.path.exists(filePath):
      for file in os.scandir(filePath):
        os.remove(file.path)
      return 'Removed All Files'
    else:
      return 'Directory Not Found'

  def RECORDERfunc(self):
    print("Start to record the audio.")

    for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
      data = self.stream.read(self.CHUNK)
      self.frames.append(data)

      if(self.recsignal == False):
        break

    print("Recording is finished.")
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()
    for i in range(0, len(self.frames)):
      ret = int.from_bytes(self.frames[i], 'little', signed=True)
      self.value.append(ret)
    self.removeAllFile('/home/pi/Desktop/ICanSeeMyVoice/recorded')
    #print(self.value)
    wf = wave.open('./resource/wav/testRecorded.wav', 'wb')
    wf.setnchannels(self.CHANNELS)
    wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
    wf.setframerate(self.RATE)
    wf.writeframes(b''.join(self.frames))
    wf.close()
  def init(self):
    self.value = []
    self.frames = []
    self.p = pyaudio.PyAudio()
    self.CHUNK = 2
    self.FORMAT = pyaudio.paInt16
    self.CHANNELS = 1
    self.RATE = 16000
    self.RECORD_SECONDS = 5
    self.recsignal = True
    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format=self.FORMAT, rate=self.RATE, channels=self.CHANNELS,
                              input_device_index=1, input=True,
                              frames_per_buffer=4096)
    '''
    self.form_1 = pyaudio.paInt16  # 16-bit resolution
    self.chans = 1  # 1 channel
    self.samp_rate = 44100  # 44.1kHz sampling rate
    self.chunk = 4096  # 2^12 samples for buffer
    self.record_secs = 3  # seconds to record
    self.dev_index = 1  # device index found by p.get_device_info_by_index(ii)

    # create pyaudio stream
    self.stream = self.p.open(format=self.form_1, rate=self.samp_rate, channels=self.chans,
                              input_device_index=self.dev_index, input=True,
                              frames_per_buffer=self.chunk)
    '''


'''
    self.form_1 = pyaudio.paInt16  # 16-bit resolution
    self.chans = 1  # 1 channel
    self.samp_rate = 44100  # 44.1kHz sampling rate
    self.chunk = 4096  # 2^12 samples for buffer
    self.record_secs = 3  # seconds to record
    self.dev_index = 1  # device index found by p.get_device_info_by_index(ii)

    # create pyaudio stream
    self.stream = self.p.open(format=self.form_1, rate=self.samp_rate, channels=self.chans,
                         input_device_index=self.dev_index, input=True,
                         frames_per_buffer=self.chunk)
     '''


