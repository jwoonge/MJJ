import pyaudio
import SoundHandler
<<<<<<< HEAD

class recorder() :
  def __init__(self):
    self.testcount = 0
    self.traincount = 0
    self.testvalue = []
    self.trainvalue = []

  def testRECORDER(self):

    self.testcount += 1
    formatname = '.wav'
    count_s = str(self.testcount)
    filename = 'test' + count_s + formatname
    CHUNK = 1
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start to record the audio.")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read(CHUNK)
      frames.append(data)

    print("Recording is finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    value = []
    for i in range(0, len(frames)):
      ret = int.from_bytes(frames[i], 'little', signed=True)
      value.append(ret)
    recorder.testvalue = value
    output_rec = SoundHandler.Sound(value, 1)
    output_rec.WriteWav_self(filename)

  def trainRECORDER(self):
    self.traincount += 1
    formatname = '.wav'
    count_s = str(self.traincount)
    filename = 'train' + count_s + formatname
    CHUNK = 1
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start to record the audio.")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read(CHUNK)
      frames.append(data)

    print("Recording is finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    value = []
    for i in range(0, len(frames)):
      ret = int.from_bytes(frames[i], 'little', signed=True)
      value.append(ret)
    recorder.trainvalue = value
    output_rec = SoundHandler.Sound(value, 1)
    output_rec.WriteWav_self(filename)
=======
import makewav
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
    wf = wave.open('test.wav', 'wb')
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

>>>>>>> GUI

