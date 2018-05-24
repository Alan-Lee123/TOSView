### GDB Config: GDBPORT

GDBPORT = '1234'

### OS config: ADDRESSBIT, SOURCEFOLDER, ASMFILE, KERNELOBJ, QEMUCOMMAND

##
# Linux config
###
ADDRESSBIT = 64
SOURCEFOLDER = '/home/alan/linux-4.16'
ASMFILE = SOURCEFOLDER + '/vmlinux.txt'
KERNELOBJ = SOURCEFOLDER + '/vmlinux'
QEMUCOMMAND = 'qemu-system-x86_64 -m 512M -kernel %s/arch/x86/boot/bzImage  \
         -initrd %s -gdb tcp::%s -S' % (SOURCEFOLDER, SOURCEFOLDER + '/initrd.img', GDBPORT)

###
# xv6 config
###
# ADDRESSBIT = 32
# SOURCEFOLDER = '/home/alan/xv6-public'
# ASMFILE = SOURCEFOLDER + '/kernel.asm'
# KERNELOBJ = SOURCEFOLDER + '/kernel'
# QEMUCOMMAND = 'qemu-system-i386 -drive \
#     file=%s/fs.img,index=1,media=disk,format=raw -drive  \
#     file=%s/xv6.img,index=0,media=disk,format=raw -m 512 -gdb tcp::%s -S' \
#     % (SOURCEFOLDER, SOURCEFOLDER, GDBPORT)


### Prune Config: PRUNED, PRUNELEVEL, PRUNEOUTCOME

PRUNED = False
PRUNELEVEL = 1
PRUNEOUTCOME = 0
