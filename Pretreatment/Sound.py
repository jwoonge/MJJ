from collections import namedtuple
import numpy as np
def Read_little_endian(num, wav_file):
    buf = wav_file.read(num)
    '''if not buf:
        return None'''
    ret = 0
    for i in range(0,num):
        ret+=buf[i]*(256**i)
    return ret

def Convert_signed(value, bitnum):
    ret = value
    if value > 2**(bitnum*8-1):
        ret -= 2**(bitnum*8)
        return ret
    return ret

class WAV_Header():
    def __init__(self):
        self.RIFF = namedtuple('Coordinate',['ChunkID', 'ChunkSize', 'Format'])
        self.FMT = namedtuple('Coordinate',['ChunkID', 'ChunkSize', 'AudioFormat','NumChannels','SampleRate','AvgByteRate','BlockAlign','BitPerSample'])          
        self.DATA = namedtuple('Coordinate',['ChunkID','ChunkSize'])

    def Make_Dummy_Header(self):
        self.RIFF.ChunkID = b'RIFF'
        self.RIFF.ChunkSize
        self.RIFF.Format = b'WAVE'

        self.FMT.ChunkID = b'fmt '
        self.FMT.ChunkSize = 18
        self.FMT.AudioFormat = 1
        self.FMT.NumChannels = 1
        self.FMT.SampleRate = 16000
        self.FMT.AvgByteRate = 16000 * 2
        self.FMT.BlockAlign = 2
        self.FMT.BitPerSample = 16

        self.DATA.ChunkID = b'data'


    def Read_WAV_Header(self, wav_file):
        self.RIFF.ChunkID = wav_file.read(4)
        self.RIFF.ChunkSize = Read_little_endian(4,wav_file)
        self.RIFF.Format = wav_file.read(4)

        self.FMT.ChunkID = wav_file.read(4)
        self.FMT.ChunkSize = Read_little_endian(4,wav_file)
        self.FMT.AudioFormat = Read_little_endian(2,wav_file)
        self.FMT.NumChannels = Read_little_endian(2,wav_file)
        self.FMT.SampleRate = Read_little_endian(4,wav_file)
        self.FMT.AvgByteRate = Read_little_endian(4,wav_file)
        self.FMT.BlockAlign = Read_little_endian(2,wav_file)
        self.FMT.BitPerSample = Read_little_endian(2,wav_file)

        while(True):
            self.DATA.ChunkID = wav_file.read(4)
            if self.DATA.ChunkID == b'data' :
                break
            wav_file.seek(-3,1)

        self.DATA.ChunkSize = Read_little_endian(4,wav_file)




class Sound():
    def __init__(self,filename):
        self.value = []
        self.value_size = 0
        self.value_count = 0
        self.Header = WAV_Header()
        self.ReadSound(filename)

    def getValue(self):
        self.npValue = np.array(self.value)
        return self.npValue
    def ReadSound(self,filename):
        with open(filename, "rb+") as wav_file:
            if '.pcm' in filename:
                self.Header.Make_Dummy_Header()
                self.stf = wav_file.tell()
                wav_file.seek(0,2)
                self.eof = wav_file.tell()
                self.value_size = 2
                self.value_count = int((self.eof-self.stf)/self.value_size)
                self.Header.DATA.ChunkSize = self.value_count * self.value_size
                self.Header.RIFF.ChunkSize = self.Header.DATA.ChunkSize + 36
                wav_file.seek(0,0)
            
            elif '.wav' in filename:
                self.Header.Read_WAV_Header(wav_file)
                self.value_size = int(self.Header.FMT.BitPerSample / 8)
                self.value_count = int(self.Header.DATA.ChunkSize / (self.value_size * self.Header.FMT.NumChannels))

            self.buffer=[]
            for i in range(0, int(self.value_count * self.Header.FMT.NumChannels)):
                self.buffer.append(Read_little_endian(self.value_size,wav_file))
        
            for i in range(0,self.value_count):
                self.value.append(Convert_signed(self.buffer[i*self.Header.FMT.NumChannels],self.value_size))
        
    def PrintHeader(self):
        print("WAV FILE Header Read")
        print("-----RIFF-----")
        print("ChunkID: ",self.Header.RIFF.ChunkID)
        print("ChunkSize: ",self.Header.RIFF.ChunkSize)
        print("Format: ",self.Header.RIFF.Format)

        print("\n-----FMT-----")
        print("ChunkID: ",self.Header.FMT.ChunkID)
        print("ChunkSize: ",self.Header.FMT.ChunkSize)
        print("AudioFormat: ",self.Header.FMT.AudioFormat)
        print("NumofChannels: ", self.Header.FMT.NumChannels)
        print("SampleRate: ",self.Header.FMT.SampleRate)
        print("AvgByteRate: ",self.Header.FMT.AvgByteRate)
        print("BlockAlign: ",self.Header.FMT.BlockAlign)
        print("BitsPerSample: ",self.Header.FMT.BitPerSample)
        print("\n-----data-----")
        print("ChunkID: ", self.Header.DATA.ChunkID)
        print("ChunkSize: ",self.Header.DATA.ChunkSize)
        print("\n-----value-----")
        print("ValueSize: ",self.value_size)
        print("ValueCount: ",self.value_count)

    def PrintValue(self):
        print("value_count: ", self.value_count)
        for i in range(0,self.value_count):
            if self.value[i] != 0:
                print(i, "\t" ,self.value[i])
    
    def WriteWav_self(self, filename):
        self.WriteWav_Mono(filename, self.value_count, self.value)

    def WriteWav_Mono(self,filename,value_count,value):
        num_channels = 1
        sample_rate = self.Header.FMT.SampleRate
        bytes_per_sample = int(self.Header.FMT.BitPerSample/8)
        byte_rate = sample_rate * bytes_per_sample * num_channels

        with open(filename,'wb') as write_file:
            #write riff
            write_file.write(b'RIFF')
            write_file.write((36 + bytes_per_sample * num_channels * value_count).to_bytes(4,byteorder='little',signed=False))
            write_file.write(b'WAVE')

            #write fmt
            write_file.write(b'fmt ')
            fmtchunksize = 16
            fmtaudioformat = 1
            write_file.write(fmtchunksize.to_bytes(4,byteorder='little',signed = False))
            write_file.write(fmtaudioformat.to_bytes(2,byteorder='little',signed = False))
            write_file.write(num_channels.to_bytes(2,byteorder='little',signed = False))
            write_file.write(sample_rate.to_bytes(4,byteorder='little',signed = False))
            write_file.write(byte_rate.to_bytes(4,byteorder='little',signed = False))
            write_file.write(num_channels*bytes_per_sample.to_bytes(2,byteorder='little',signed = False))
            write_file.write(self.Header.FMT.BitPerSample.to_bytes(2,byteorder='little',signed = False))

            #write data
            write_file.write(b'data')
            write_file.write((bytes_per_sample*value_count*num_channels).to_bytes(4,byteorder='little',signed = False))

            for i in range(0,value_count*num_channels):
                write_file.write(value[i].to_bytes(bytes_per_sample,byteorder='little',signed=True))

    def DoTest(self):
        self.newArray = []
        for i in range(int(self.value_count /2), self.value_count):
            self.newArray.append(self.value[i])
        self.WriteWav_Mono("testWrite.wav",len(self.newArray),self.newArray)