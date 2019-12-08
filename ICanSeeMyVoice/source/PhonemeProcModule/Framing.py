import math

def Framing(input_list, frame_size, interval):
    value_count = len(input_list)
    N_frames = math.ceil((value_count-frame_size)/(frame_size-interval))
    framed_list = [[0 for x in range(frame_size)] for y in range(N_frames)]
    for i in range(N_frames):
        for j in range(frame_size):
            framed_list[i][j] = input_list[i*(frame_size-interval)+j]

    return framed_list

def Framing_2dim(input, frame_size, interval):
    value_count = len(input)
    freqs = len(input[0])
    N_frames = math.ceil((value_count-frame_size)/(frame_size-interval))
    framed_list = []
    for i in range(N_frames):
        temp = [0 for x in range(frame_size)]
        for j in range(frame_size):
            temp[j] = input[i*(frame_size-interval)+j]
        temp_1dim = [0 for x in range(freqs)]
        for j in range(frame_size):
            for k in range(freqs):
                temp_1dim[k] += temp[j][k]/frame_size
        framed_list.append(temp_1dim)
    return framed_list
        

            

def Get_Frames(original_list, start, end, frame_size, interval):
    ret = []
    if start > end:
        return ret
    elif start < 0:
        return ret
    startIndex = Index_frame_to_origin(start,frame_size,interval)
    endIndex = Index_frame_to_origin(end,frame_size,interval) + frame_size -1

    for i in range(startIndex, endIndex):
        if i<len(original_list):
            ret.append(original_list[i])
            
    return ret
    
def Index_frame_to_origin(index, frame_size, interval):
    startIndex = index*(frame_size-interval)

    return startIndex