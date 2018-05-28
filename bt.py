def parse_bt(ls):
    l = ' '.join(ls)
    tbts = l.split('#')[1:]
    bts = []
    num = 0
    for bt in tbts:
        tmp = bt.split()[0]
        if(tmp.isdigit() and int(tmp) == num):
            bts.append(bt)
            num += 1
        elif(len(bts) > 0):
            bts[-1] += bt
        
    infos = []
    for bt in bts:
        left = bt.index('(')
        right = bt.rindex(')')
        bt = bt[:left] + bt[right + 1:]
        ws = bt.split()
        start = 1
        if(len(ws) > 2 and ws[2] == 'in'):
            start = 3
        func = ws[start]
        start += 1
        file = ''
        line = ''
        if(start < len(ws) and ws[start] == 'at'):
            tmp = ws[start + 1].split(':')
            file, line = tmp[0], tmp[1]
        

        infos.append([func, file, line])
    return infos

def cmp_bt(bt, base):
    n = len(base)
    if(len(bt) >= n):
        if(n == 1):
            return bt[-1][:2] == base[0][:2]
        elif(bt[-n + 1:] == base[1:] and
            bt[-n][:2] == base[0][:2]):
            return True
    return False

def common_bt(cur, pre, n):
    x = -n 
    m = -min(len(cur), len(pre))
    while(x >= m and cur[x][:2] == pre[x][:2]):
        x -= 1
    return len(cur) + x + 1

