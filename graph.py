from bt import common_bt
class graphPainter:
    def __init__(self, fname, base_bt, sourceFolder, depth):
        self.f = open(fname, 'w')
        self.existLinks = {}
        self.f.write('digraph {\n')
        self.base_bt = base_bt
        self.pre_bt = base_bt
        self.sourceFolder = sourceFolder + '/'
        self.maxDepth = depth
        self.nodes = {}
        self.cnt = 0

    def insert(self, key, n):
        if(key not in self.nodes.keys()):
            self.nodes[key] = 'n' + str(len(self.nodes.keys()))
            self.f.write(self.nodes[key] + ' [label = %s URL = %s];\n' % 
                (key[:-1] + ':' + n + '"', '"' + self.sourceFolder + key.split('\\n')[1]))
    
    def paint(self, bt, new):
        height = len(bt) - len(self.base_bt)
        if(height <= 0):
            return
        top = common_bt(bt, self.pre_bt, len(self.base_bt))
        if(new):
            top = max(top, 1)
        cur = '"' +  bt[top][0] + '\\n' + bt[top][1] + '"'
        self.insert(cur, bt[top][2])
        while(height - top < self.maxDepth and top > 0):
            top -= 1
            pre = cur
            cur = '"' +  bt[top][0] + '\\n' + bt[top][1] + '"'
            self.insert(cur, bt[top][2])
            link = self.nodes[pre] + ' -> ' + self.nodes[cur]
            self.cnt += 1
            if(link not in self.existLinks.keys()):
                self.existLinks[link] = [self.cnt]
            else:
                self.existLinks[link].append(self.cnt)
        self.pre_bt = bt

    def close(self):
        for link in sorted(self.existLinks.keys()):
            if(len(self.existLinks[link]) <= 5):
                label = ','.join([str(n) for n in self.existLinks[link]])
            else:
                ns = self.existLinks[link][:5]
                label = ','.join([str(n) for n in ns]) + ',...'
            self.f.write('%s [label = "%s"];\n' % (link, label))
        self.f.write("}\n")
        self.f.close()
