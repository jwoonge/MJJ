import pyaudio
import SoundHandler

def testRECORDER() :
  testRECORDER.count += 1
  formatname='.wav'
  count_s = str(testRECORDER.count)
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

  output_rec = SoundHandler.Sound(value, 1)
  output_rec.WriteWav_self(filename)

def trainRECORDER() :
  trainRECORDER.count += 1
  formatname='.wav'
  count_s = str(testRECORDER.count)
  filename = 'train' + count_s + formatname
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

  output_rec = SoundHandler.Sound(value, 1)
  output_rec.WriteWav_self(filename)


trainRECORDER.count = 0
testRECORDER.count = 0