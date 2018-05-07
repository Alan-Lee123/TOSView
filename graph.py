
class graphPainter:
    def __init__(self, fname, base_bt, sourceFolder, depth):
        self.f = open(fname, 'w')
        self.existLinks = set()
        self.f.write('digraph {\n')
        self.base_bt = base_bt
        self.sourceFolder = sourceFolder + '/'
        self.maxDepth = depth
        self.nodes = {}
        self.cnt = 0

    def insert(self, key, n):
        if(key not in self.nodes.keys()):
            self.nodes[key] = 'n' + str(len(self.nodes.keys()))
            self.f.write(self.nodes[key] + ' [label = %s URL = %s];\n' % 
                (key[:-1] + ':' + n + '"', '"' + self.sourceFolder + key.split('\\n')[1]))
    
    def paint(self, bt):
        height = len(bt) - len(self.base_bt)
        top = height
        cur = '"' +  bt[top][0] + '\\n' + bt[top][1] + '"'
        self.insert(cur, bt[top][2])
        while(height - top < self.maxDepth and top > 0):
            top -= 1
            pre = cur
            cur = '"' +  bt[top][0] + '\\n' + bt[top][1] + '"'
            self.insert(cur, bt[top][2])
            link = self.nodes[pre] + ' -> ' + self.nodes[cur]
            if(link not in self.existLinks):
                self.existLinks.add(link)
                self.cnt += 1
                link += ' [label = "%d"];\n' % self.cnt
                self.f.write(link)
                

    def close(self):
        self.f.write("}\n")
        self.f.close()
