import pyaudio
import SoundHandler

class recorder() :
  def __init__(self):
    self.testcount = 0
    self.traincount = 0
    self.testvalue = []
    self.trainvalue = []

  def testRECORDER(self):

    self.testcount += 1
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

  def trainRECORDER(self):
    self.traincount += 1
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

