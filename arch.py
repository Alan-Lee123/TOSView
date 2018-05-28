def getArch(arch):
    dt = {'x86_64': x86_64_arch, 'i386': i386_arch}
    return dt[arch](arch)


class base_arch:
    def __init__(self, arch):
        self._arch = arch
    def getBit(self):
        pass
    def getRets(self):
        pass
    def getEip(self):
        pass

class x86_64_arch(base_arch):
    def getBit(self):
        return 64
    def getRets(self):
        return [['retq']]
    def getEip(self):
        return 'rip'

class i386_arch(base_arch):
    def getBit(self):
        return 32
    def getRets(self):
        return [['ret'], ['leave'], ['pop', '%ebp']]
    def getEip(self):
        return 'eip'
    
