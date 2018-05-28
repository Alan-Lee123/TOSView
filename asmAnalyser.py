import string
import time
import os
from config import ARCH
from arch import getArch

class asmAnalyser:
    def __init__(self, addr):

        self.calls = {}
        self.rets = {}
        self.callDsts = {}
        self.funcAddrs = {}
        ah = getArch(ARCH)
        self.BIT = ah.getBit() // 4
        self.RET = ah.getRets()

        tracerFile = addr.split('/')[-1] + '.tracer'
        if(not self.load(tracerFile, addr)):
            self.analyze(addr)
            self.save(tracerFile, addr)

    
    def load(self, tracerFileName, asmFileName):
        cur = -1
        if(not os.path.isfile(tracerFileName)):
            return False
        with open(tracerFileName) as f:
            ls = f.readlines()
            if(ls[0].strip() != str(os.path.getmtime(asmFileName))):
                return False
            for l in ls[1:]:
                if(l[0] == '#'):
                    if('rets' in l):
                        cur = 0
                    elif('calls' in l):
                        cur = 1
                    elif('callDsts' in l):
                        cur = 2
                    elif('funcAddrs' in l):
                        cur = 3
                else:
                    ws = l.strip().split(':')
                    if(cur == 0):
                        self.rets[ws[0]] = ws[1:]
                    elif(cur == 1):
                        self.calls[ws[0]] = ws[1:]
                    elif(cur == 2):
                        self.callDsts[ws[0]] = ws[1]
                    elif(cur == 3):
                        self.funcAddrs[ws[0]] = ws[1]
        return True
    
    def save(self, tracerFileName, asmFileName):
        f = open(tracerFileName, 'w')
        f.write(str(os.path.getmtime(asmFileName)) + '\n')
        f.write('#rets:\n')
        for fname in self.rets:
            f.write(fname)
            for r in self.rets[fname]:
                f.write(':' + r)
            f.write('\n')
        f.write('#calls:\n')
        for fname in self.calls:
            f.write(fname)
            for call in self.calls[fname]:
                f.write(':' + call)
            f.write('\n')
        f.write('#callDsts:\n')
        for addr in self.callDsts:
            f.write(addr + ':' + self.callDsts[addr] + '\n')
        f.write('#funcAddrs:\n')
        for func in self.funcAddrs:
            f.write(func + ':' + self.funcAddrs[func] + '\n')
        f.close()

    
    def analyze(self, fName):
        def beginWithHex(s):
            return all(c in string.hexdigits for c in s[:self.BIT])
        
        def dst(d):
            s = d.split()[-1]
            s = s[1:].replace('%', '$')
            s = s.replace(')', '').replace('(', '+')
            return s
        
        def checkRet(ws):
            for ret in self.RET:
                if(all(w in ws for w in ret)):
                    return True
            return False
                     
        
        with open(fName) as f:
            name = ''
            for l in f:
                l = l.strip()
                ws = l.split()
                if(len(l) < self.BIT or not beginWithHex(l)):
                    name = ''
                    continue 
                elif(l[self.BIT] == ' '):
                    name = l[l.index('<') + 1: l.index('>')]
                    self.calls[name] = []
                    self.rets[name] = []
                    funcAddr = '0x' + l[:self.BIT]
                    self.funcAddrs[name] = funcAddr
                elif(l[self.BIT] == ':'):
                    addr = '0x' + l[:self.BIT]
                    if('#' in l):
                        l = l[:l.index('#')]
                    b = False
                    if('*' in l ):
                        b = True
                        self.callDsts[addr] = dst(l)
                        target = '*' + addr
                    elif('<' in l and '>' in l):
                        cur = l[l.index('<') + 1: l.index('>')]
                        if('+' in cur):
                            cur = cur.split('+')[0]
                        if(cur != name):
                            b = True
                            target = '*0x' + ws[-2]
                    elif(checkRet(ws)):
                        self.rets[name] += ['*' + addr]
                    if(b == True and addr != funcAddr):
                        self.calls[name] += [target]

    def getCalls(self, func):
        return self.calls[func]
    
    def getRets(self, func):
        return self.rets[func]
    
    def getCallDst(self, addr):
        return self.callDsts[addr]
    
    def getCallSrcs(self):
        return self.callDsts.keys()
    
    def getFuncAddr(self, func):
        return self.funcAddrs[func]
    
    def funcExist(self, func):
        return func in self.calls.keys()


if __name__=='__main__':
    start = time.clock()
    asm = asmAnalyser('/home/alan/xv6-public/kernel.asm')
    print(time.clock() - start)
    print('call func, ret func, callDst addr')
    while(True):
        ws = input().split()
        if(ws[0] == 'call'):
            print(sorted(asm.getCalls(ws[1])))
        elif(ws[0] == 'ret'):
            print(sorted(asm.getRets(ws[1])))
        elif(ws[0] == 'callDst'):
            print(asm.getCallDst(ws[1]))
        else:
            break
		
	
		
	
		
	
		
	
		
	
		
	
		
	
	
