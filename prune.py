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
    topics = LEVELTABLE[0].copy()
    for k in range(1, PRUNELEVEL + 1):
        topics += LEVELTABLE[k].copy()
    
    outcome = set(OUTCOMETABLE[PRUNEOUTCOME])
    topics = set(topics).intersection(outcome)
    validFiles = set()
    for t in topics:
        for f in FILETABLE[t]:
            validFiles.add(f)
    
    parent = {}
    validNodes = set()
    validNodes.add('n0')

    def valid(x, n):
        if(x in validNodes):
            return [x, n]
        else:
            r = ['', 0]
            for p in parent[x]:
                if(p[1] < n and p[1] > r[1]):
                    r = p
            return valid(r[0], r[1])

    prunedFile = open(prunedFileName, 'w')

    with open(dotFileName, 'r') as f:
        ls = f.readlines()
    
    prunedFile.write(ls[0])
    prunedFile.write(ls[1])

    for l in ls[2:]:
        ws = l.split()
        if(len(ws) == 6):
            p = ws[0]
            s = ws[2]
            ns = ws[5].split('"')[1].split(',')
            for t in ns:
                if t != '...':
                    if(s not in parent.keys()):
                        parent[s] = [[p, int(t)]]
                    else:
                        parent[s].append([p, int(t)])

        elif(len(ws) == 7):
            fname = ws[3].split('\\n')[1].split(':')[0]
            flag = fname in validFiles
            if(len(fname) > 2 and fname[:2] == './'):
                start = 2
            else:
                start = 0
            for k in range(start, len(fname)):
                if(fname[k] == '/'):
                    if(fname[start:k + 1] in validFiles):
                        flag = True
            if(flag):
                validNodes.add(ws[0])
                nl = ' '.join(ws)
                prunedFile.write(nl + '\n')
    

    for l in ls[2:]:
        ws = l.split()
        if(len(ws) == 6):
            if(ws[2] in validNodes):
                ns = ws[5].split('"')[1].split(',')
                ps = {}
                for n in ns:
                    if(n == '...'):
                        continue
                    n = int(n)
                    p = valid(ws[0], n)
                    if(len(p) > 0):
                        if(p[1] != n):
                            p[1] = '%d-%d' % (p[1], n)
                        else:
                            p[1] = str(p[1])
                        if(p[0] not in ps.keys()):
                            ps[p[0]] = [p[1]]
                        else:
                            ps[p[0]].append(p[1])
                    
                for p in ps.keys():
                    ws[0] = p
                    ws[5] = '"%s"];' % ','.join(ps[p])
                    nl = ' '.join(ws)
                    prunedFile.write(nl + '\n')

    prunedFile.write(ls[-1])
    prunedFile.close()


