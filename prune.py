from pruneConfig import *
from config import PRUNED, PRUNELEVEL, PRUNEOUTCOME

def pruneCheck():
    topics = []
    for t in LEVELTABLE:
        topics += t
    topics.sort()
    assert(topics == list(range(len(topics))))
    assert(PRUNELEVEL < len(LEVELTABLE))
    assert(PRUNEOUTCOME < len(OUTCOMETABLE))
    for l in OUTCOMETABLE:
        for t in l:
            assert(t < TOPICNUMBERS and t >= 0)
    assert(len(FILETABLE) == TOPICNUMBERS)
    

def prune(dotFileName, prunedFileName):
    pruneCheck()
    topics = LEVELTABLE[0]
    for k in range(1, PRUNELEVEL + 1):
        topics += LEVELTABLE[k]
    
    outcome = set(OUTCOMETABLE[PRUNEOUTCOME])
    topics = set(topics).intersection(outcome)
    validFiles = set()
    for t in topics:
        for f in FILETABLE[t]:
            validFiles.add(f)
    
    parent = {}
    validNodes = set()
    validNodes.add('n0')

    def valid(x):
        if(x in validNodes):
            return x
        else:
            return valid(parent[x])
    
    prunedFile = open(prunedFileName, 'w')
    with open(dotFileName, 'r') as f:
        ls = f.readlines()
        for l in ls:
            ws = l.split()
            if(len(ws) == 3):
                ws = l.split()
                p = ws[0]
                s = ws[2].split(';')[0]
                parent[s] = p
                if(s in validNodes):
                    ws[0] = valid(p)
                    nl = ' '.join(ws)
                    prunedFile.write(nl + '\n')
            elif(len(ws) == 7):
                fname = ws[3].split('\\n')[1].split(':')[0]
                if(fname in validFiles):
                    validNodes.add(ws[0])
                    nl = ' '.join(ws)
                    prunedFile.write(nl + '\n')
            else:
                prunedFile.write(l)
    prunedFile.close()

