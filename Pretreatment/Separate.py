from PhonemeProc import PhonemeProc
import sys


fileDir = sys.argv[1]
Graph = False
debug = False
Remove_Write = False
pcmwav = "pcm"
Separate = False


if 'g' in sys.argv:
    Graph = True
if 'd' in sys.argv:
    debug = True
if 'r' in sys.argv:
    Remove_Write = True
if 's' in sys.argv:
    Separate = True

Proc = PhonemeProc()

if not '-' in sys.argv[1]:
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

        Proc.DoProcess(fileDir = fileDir, pcmwav = pcmwav, debug=debug, separate=Separate,Graph =Graph)
    
    else:
        Proc.DoProcess(int(sys.argv[1]), debug =debug,separate=Separate, Graph =Graph)

else:
    start = ""
    end = ""
    barpoint = 0
    for i in range(len(sys.argv[1])):
        if sys.argv[1][i] == '-':
            barpoint = i
            break
    for i in range(barpoint):
        startC+=str(sys.argv[1][i])
    for i in range(barpoint+1, len*sys.argv[1]):
        endC+=str(sys.argv[1][i])
   
    start = int(start)
    end = int(end)

    if start > end :
        end = start
    HitCount = 0

    for i in range(start+1,end+1):
        if Proc.DoProcess(i, debug = debug, separate=Separate, Graph = Graph):
            HitCount+=1
    print("Total : ",end-start,"\tHit : ",HitCount,"\tHitRate : ",HitCount/(end-start))