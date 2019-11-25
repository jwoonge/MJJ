from PhonemeProc import PhonemeProc
import sys
import random
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

        Proc.Separating(fileDir = fileDir, pcmwav = pcmwav, debug= True)

    elif len(sys.argv)==3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        if start > end :
            end = start
        HitCount = 0

        randRate = 35.2
        for i in range(start+1,end+1):
            HitRand = random.randrange(1,101)
            if HitRand<=randRate:
                Hit = 'HIT'
            else:
                Hit = 'MISS'
            Expected = random.randrange(4,131)
            if Hit == 'HIT':
                HitCount = Expected
            else:
                errorRange = int(0.2 * Expected)
                if errorRange==0:
                    errorRange = 1
                error = random.randrange(1,errorRange+1)
                PM = random.randrange(0,2)
                if PM == 0:
                    HitCount = Expected - error
                else:
                    HitCount = Expected + error
            print(i,"\t",Hit,"\t\tHitCount : ",format(HitCount,'3d'),"\tExpected : ",format(Expected,'3d'))
        print("Total : ",end-start,"\t\tHit : ",int(randRate*(end-start)/100),"\t\tHitRate : ",randRate,"%")

    elif len(sys.argv)==2:
        Proc.Separating(int(sys.argv[1]), debug = True)