from bt import parse_bt, cmp_bt
from graph import graphPainter
from asmAnalyser import asmAnalyser
import time
from config import LINUXFOLDER, ASMFILE

class gdbTracer:
    def __init__(self, p, funcName):
        self.p = p
        self.func = funcName
        self.sourceFolder = LINUXFOLDER
        self.max_brkTime = 30    # If a breakpoint is triggered more than this number, it will be removed
        self.ed = '394743516231415926'   # A random number as end of output of a session

        print('loading %s' % ASMFILE)
        cur_time = time.clock()
        self.asm = asmAnalyser(ASMFILE)
        print('finished loading, cost %ss' % str(time.clock() - cur_time))
        if(not self.asm.funcExist(funcName)):
            print('ERROR! Function %s not exist!' % funcName)
            return
        p.stdin.write(bytes('target remote:1234\n', encoding='utf8'))

    
    def configure(self, dotFileName, logFileName, depth):
        self.dotFileName = dotFileName
        self.log = open(logFileName, 'w')
        self.maxDepth = depth
        self.endAddrs = []
        self. existBreakpoints = set()
        self.brks = {}

    def flush(self):
        self.write('p ' + self.ed)
        self.p.stdin.flush()
    
    def write(self, s):
        self.p.stdin.write(bytes(s + '\n', encoding='utf8'))
        self.log.write(s + '\n')

    def read(self):
        ls = []
        while(True):
            l = self.p.stdout.readline().decode()
            ls.append(l)
            if(self.ed in l):
                break
        self.log.writelines(ls)
        ls.pop()
        return ls
    
    def getRip(self):
        self.write('p/x $rip')
        self.flush()
        ls = self.read()
        assert(len(ls) > 0 and '= ' in ls[-1])
        return ls[-1].split('= ')[-1].strip()
        
    
    def bk(self, point):
        if(point[0] != '*'):
            self.write('p/x %s' % point)
            self.flush()
            ls = self.read()
            assert(len(ls) > 0 and '=' in ls[-1])
            point = '*' + ls[-1].split('= ')[-1].strip()
        
        if(point not in self.existBreakpoints):
            self.write('b %s' % point)
            self.existBreakpoints.add(point)

    def checkBreak(self, ls):
        b = 'Breakpoint'
        lb = len(b)
        bn = -1
        for l in ls:
            if(len(l) > lb and l[:lb] == b):
                bn = int(l.split(',')[0].split()[1])
                break
        assert(bn != -1)
        if(bn in self.brks.keys()):
            self.brks[bn] += 1
        else:
            self.brks[bn] = 1
        if(self.brks[bn] > self.max_brkTime):
            self.write('d %d' % bn)
            
    
    def run(self):
        self.write('delete')
        self.write('b ' + self.func)
        self.write('c')
        self.write('bt 100')
        self.flush()

        ls = self.read()
        bt = parse_bt(ls)
        base_bt = bt
        rip = self.getRip()
        func = bt[0][0]
        assert(func == self.func)
        for point in self.asm.getRets(func):
            self.endAddrs.append(point[1:])
        painter = graphPainter(self.dotFileName, bt, self.sourceFolder, self.maxDepth)
        

        while(True):
            if(cmp_bt(bt, base_bt)):
                painter.paint(bt)
                if(rip in self.endAddrs):
                    break
                if(len(bt) - len(base_bt) <= self.maxDepth):
                    if(self.asm.funcExist(func) and rip == self.asm.getFuncAddr(func)):
                        for point in (self.asm.getRets(func) + self.asm.getCalls(func)):
                            self.bk(point)
                    if(rip in self.asm.getCallSrcs()):
                        self.bk(self.asm.getCallDst(rip))
            
            self.write('c')
            self.write('bt 100')
            self.flush()
            ls = self.read()
            bt = parse_bt(ls)
            rip = self.getRip()
            func = bt[0][0]
            self.checkBreak(ls)
        
        painter.close()
        self.log.close()

            


        
