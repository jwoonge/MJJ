import numpy as np
import os

def Write_wav(filename, input, sample_rate=16000, value_size=2, num_channels=1):
    bytes_per_sample = value_size
    bits_per_sample = bytes_per_sample * 8
    byte_rate = sample_rate * bytes_per_sample * num_channels
    value_count = len(input)

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
        write_file.write(bits_per_sample.to_bytes(2,byteorder='little',signed = False))

        #write data
        write_file.write(b'data')
        write_file.write((bytes_per_sample * value_count * num_channels).to_bytes(4,byteorder='little',signed=False))

        for i in range(0,value_count*num_channels):
            if input[i]>32767:
                input[i] = 32767
            elif input[i]<-32768:
                input[i] = -32768
        for i in range(0, value_count*num_channels):
            write_file.write(input[i].to_bytes(bytes_per_sample,byteorder='little',signed=True))

def removeAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
        return 'Removed All Files'
    else:
        return 'Directory Not Found'

def Read_file(filename):
    with open(filename, "rb+") as read_file:
        value_size=0
        value_count=0
        sample_rate = 0
        num_channels = 1
        if '.pcm' in filename:
            stf = read_file.tell()
            read_file.seek(0,2)
            eof = read_file.tell()
            value_size = 2
            sample_rate = 16000
            value_count = int((eof-stf)/value_size)
            read_file.seek(0,0)

        elif '.wav' in filename:
            readRIFF = read_file.read(12)
            readfmt1 = read_file.read(10)
            num_channels = Read_little_endian(2,read_file)
            sample_rate = Read_little_endian(4,read_file)
            readfmt2 = read_file.read(6)
            value_size = int(Read_little_endian(2,read_file) / 8)
            while(True):
                ChunkID = read_file.read(4)
                if ChunkID == b'data' :
                    break
                read_file.seek(-3,1)
            value_count = int(Read_little_endian(4,read_file) / (num_channels * value_size))
        buffer = []
        value = []
        for i in range(0,value_count*num_channels):
            buffer.append(Read_little_endian(value_size,read_file))

        for i in range(0,value_count):
            value.append(Convert_signed(buffer[i*num_channels],value_size))


        return value, sample_rate

        


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
