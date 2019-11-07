from PhonemeProc import PhonemeProc
import sys
Proc = PhonemeProc()

if not len(sys.argv) == 1:
    if '.' in sys.argv[1]:
        fileDir = ""
        pcmwav = ""
        DotPoint = 0
        for i in range(len(sys.argv[1])):
            fileDir += str(sys.argv[1][i])
            if sys.argv[1][i+1] == '.':
                DotPoint = i+1
                break
        for i in range(DotPoint+1, len(sys.argv[1])):
            pcmwav+=str(sys.argv[1][i])
        print(fileDir)
        print(pcmwav)

        Proc.Separating(fileDir = fileDir, pcmwav = pcmwav)

    elif len(sys.argv)==3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        if start > end :
            end = start
        HitCount = 0

        for i in range(start+1,end+1):
            if Proc.Separating(i):
                HitCount+=1
        print("Total : ",end-start,"\tHit : ",HitCount,"\tHitRate : ",HitCount/(end-start))

    elif len(sys.argv)==2:
        Proc.Separating(int(sys.argv[1]))