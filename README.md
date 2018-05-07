# linux-kernel-code-reader
Draw the running traces of linux kernel functions in a graph and link graph nodes to the source codes

![alt text](https://github.com/Alan-Lee123/linux-kernel-code-reader/blob/master/trace.png)

# Why you need this
If you try reading linux kernel source code, you
will find that you are sinking into the sea of codes. It is hard to figure out where the definition of a function or a macro is (from dozens of different definitions with the same name), not to mention a function pointer's actually meanning.

Using gdb seems a good idea, but typing "break" and "continue" all the time is boring and inefficient.

While this project types "break" and "continue" for you automaticly, and draw the running traces of linux kernel functions in a graph. You can open the graph with a browser like Firefox and click the nodes of the graph to see the corresponding source codes.

# Dependencies
1. A linux distribution (ubuntu is recommemended)
2. [linux kernel source code](https://www.kernel.org/)
3. qemu
4. gdb (please see the following section for more infomations on gdb)
5. python3

# Install
1. Compile linux kernel source code
    1. make mrproper
    2. make defconfig
    3. make menuconfig
        1. open "64-bit kernel"
        2. Close "Processor type and features/Randomize the address of the kernel image (KALSR)"
        3. in "Kernel hacking/Compile-time checks and compiler options"
            1. open "Compile the kernel with debug info"
            2. close "Reduce debug information"
            3. clode "Provide split debuginfo in .dwo files"
            4. open "Generate dwarf4 debuginfo"
            5. open "Provide GDB scripts for kernel debugging"
            6. open "Generate readable assembler code"
            7. open "Debug Filesystem"
    4. save and quit menuconfig
    5. make -j* (* means the cpu cores your computer have)
    6. make modules
2. You can find "vmlinux" in your linux kernel source code folder after compiling. Run:   
    1. objdump -d vmlinux > vmlinux.txt
3. Create initrd
    1. mkinitramfs -o initrd.img
4. Open linux-kernel-code-reader/config.py, change the configuration.
    1. LINUXFOLDER is address of your linux kernel source code folder
    2. ARCH should be "x86", this project do not support other archetecture now.
    3. QEMU should be "qemu-system-x86_64" for the same reason
    4. MEMORYSIZE is the memory size you want your qemu to simulate, it should not be too small
    5. INITRDADDR is the address of your initrd.img
    6. ASMFILE is the address of your vmlinux.txt

### gdb
    If you debug linux kernel with the official version of gdb, you will encounter a problem: "Remote 'g' packet reply is too long", so you need to download gdb source code, fix this problem and rebuild it.

    change function process_g_packet in gdb/remote.c from 

    if (buf_len > 2 * rsa->sizeof_g_packet)
        error (_(“Remote ‘g’ packet reply is too long: %s”), rs->buf);

    to

    if (buf_len > 2 * rsa->sizeof_g_packet) {
        rsa->sizeof_g_packet = buf_len ;
        for (i = 0; i < gdbarch_num_regs (gdbarch); i++)  
        {
            if (rsa->regs->pnum == -1)
                continue;
            if (rsa->regs->offset >= rsa->sizeof_g_packet)
                rsa->regs->in_g_packet = 0;
            else  
                rsa->regs->in_g_packet = 1;
        }     
    }

    Then, compile and install gdb:
    ./configure
    make
    sudo make install 


    Note: this change will work for gdb 8.1. For different version of gdb, the change may be slightly different ([for example](https://blog.csdn.net/u013592097/article/details/70549657)). If you can compile gdb after the change, it should work.


# Run
    python3 linux-kernel-code-reader/pyTracer.py functionYouWantToTrace
