import sys
import subprocess
import time
import os
import signal
import shutil

from bt import parse_bt, cmp_bt
from threading import Thread
from graph import graphPainter
from gdb import gdbTracer
from config import QEMUCOMMAND, SOURCEFOLDER, KERNELOBJ
from prune import prune
from config import PRUNED


if __name__=='__main__':
    funcName = sys.argv[1]
    qemu_p = subprocess.Popen(QEMUCOMMAND, shell=True, preexec_fn=os.setsid)
    g = subprocess.Popen('gdb ' + KERNELOBJ, shell=True, stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

    if  os.path.exists('result'):
        shutil.rmtree('result')
    os.makedirs('result')

    logCnt = 0
    gt = gdbTracer(g, funcName)

    while True:
        dotFileName = 'result/trace%d.dot' % logCnt
        svgFileName = 'result/trace%d.svg' % logCnt
        logFileName = 'result/log%d.txt' % logCnt
        print('input the max depth of calling tree: (max means no limit)')
        r = input()
        if('max' in r.lower()):
            maxDepth = 1000000
        else:
            maxDepth = int(r.strip())
        gt.configure(dotFileName, logFileName, maxDepth)
        try:
            gt.run()
        except Exception as e:
            print(e)
            gt.painter.close()
            gt.log.close()
            
            
        subprocess.Popen('dot -Tsvg %s -o %s' %(dotFileName, svgFileName), shell=True)
        if(PRUNED):
            prunedDotFileName = dotFileName.split('.')[0] + '_pruned.dot'
            prunedSvgFileName = svgFileName.split('.')[0] + '_pruned.svg'
            prune(dotFileName, prunedDotFileName)
            subprocess.Popen('dot -Tsvg %s -o %s' %(prunedDotFileName, prunedSvgFileName), shell=True)

        print('Finish ploting %s' % svgFileName)
        print('Continue and plot another graph on %s?(n/y)' % funcName)
        r = input()
        if(r.lower() != 'y'):
            break

        logCnt += 1
    
    os.killpg(os.getpgid(g.pid), signal.SIGTERM)
    os.killpg(os.getpgid(qemu_p.pid), signal.SIGTERM)



    