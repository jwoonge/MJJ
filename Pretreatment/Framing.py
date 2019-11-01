import math

def Framing(input_list, frame_size, interval):
    value_count = len(input_list)
    N_frames = math.ceil((value_count-frame_size)/(frame_size-interval))+1
    framed_list = [[0 for x in range(frame_size)] for y in range(N_frames)]
    for i in range(N_frames-1):
        for j in range(frame_size):
            framed_list[i][j] = input_list[i*(frame_size-interval)+j]
    for i in range((N_frames-1)*(frame_size-interval), value_count):
        framed_list[N_frames-1][i-(N_frames-1)*(frame_size-interval)] = input_list[i]

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