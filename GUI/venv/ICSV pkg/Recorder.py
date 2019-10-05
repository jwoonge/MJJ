import pyaudio
import SoundHandler
import makewav

class recorder() :
  def __init__(self):
    self.value = []
    self.CHUNK = 1
    self.FORMAT = pyaudio.paInt16
    self.CHANNELS = 1
    self.RATE = 16000
    self.RECORD_SECONDS = 10
    self.frames = []
    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)
    self.recsignal = True

  def RECORDERfunc(self):
    print("Start to record the audio.")

    for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
      data = self.stream.read(self.CHUNK)
      self.frames.append(data)
      print(len(self.frames))
      if(self.recsignal == False):
        break

    print("Recording is finished.")
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()
    print(len(self.frames))
    for i in range(0, len(self.frames)):
      ret = int.from_bytes(self.frames[i], 'little', signed=True)
      self.value.append(ret)
    print(len(self.value))
    makewav.Write_wav('test니미.wav',self.value)

  def init(self):
    self.value = []
    self.CHUNK = 1
    self.FORMAT = pyaudio.paInt16
    self.CHANNELS = 1
    self.RATE = 16000
    self.RECORD_SECONDS = 10
    self.frames = []
    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format=self.FORMAT,
                              channels=self.CHANNELS,
                              rate=self.RATE,
                              input=True,
                              frames_per_buffer=self.CHUNK)
    self.frames = []
    self.recsignal = True



