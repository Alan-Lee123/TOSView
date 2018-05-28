# Topics (of filesystem):
#0 data
#1 metadata
#2 operations
#3 organization
#4 buffering
#5 sequential
#6 nonsequential
#7 directories
#8 partitioning
#9 mount/unmount
#10 virtual file systems
#11 Standard implementation techniques
#12 Memory-mapped files
#13 Special-purpose file systems
#14 Naming, searching
#15 access
#16 backups
#17 Journaling and log-structured file systems


# Learning outcomes
#0 Describe the choices to be made in designing file systems.
#1 Compare and contrast different approaches to file organization, recognizing the strengths and weaknesses
#   of each.
#2 Summarize how hardware developments have led to changes in the priorities for the design and the
#   management of file systems.
#3 Summarize the use of journaling and how log-structured file systems enhance fault tolerance.


TOPICNUMBERS = 18
LEVELTABLE = [[2, 7, 9, 14, 15, 16],
                    [0, 1, 3, 4, 5, 6, 8, 10],
                    [11, 12, 13, 17]]
OUTCOMETABLE = [[0, 1, 2, 3, 4, 7, 8, 10, 14, 15, 16],
                    [3, 7, 8],
                    [3, 4, 5, 6, 9, 11, 12, 13],
                    [17]]

FILETABLE = [['fs/binfmt_aout.c', 'fs/binfmt_elf_fdpic.c', 'fs/binfmt_elf.c', 
'fs/binfmt_em86.c', 'fs/binfmt_flat.c', 'fs/binfmt_misc.c', 'fs/binfmt_script.c', 'fs/compat_binfmt_elf.c'],
            ['fs/attr.c', 'fs/fhandle.c', 'fs/file_table.c', 'fs/file.c', 'fs/stat.c', 'fs/statfs.c', 'fs/xattr.c', 
'fs/ext2/xattr_security.c', 'fs/ext2/xattr_trusted.c', 'fs/ext2/xattr_user.c', 'fs/ext2/xattr_user.c', 
'fs/ext2/xattr.c', 'fs/ext2/xattr.h'],
            ['fs/aio.c', 'fs/direct-io.c', 'fs/exec.c', 'fs/fcntl.c', 'fs/fs-writeback.c', 'fs/libfs.c',
'fs/mpage.c', 'fs/open.c', 'fs/read_write.c', 'fs/splice.c', 'fs/sync.c'],
            ['fs/inode.c', 'fs/super.c', 'fs/ext2/balloc.c', 'fs/ext2/ialloc.c', 'fs/ext2/inode.c', 'fs/ext2/super.c'],
            ['fs/buffer.c', 'fs/dcache.c', 'fs/drop_caches.c', 'fs/mbcache.c', 'fs/cachefiles/'],
            ['fs/char_dev.c', 'fs/pipe.c', 'fs/seq_file.c'],
            ['fs/block_dev.c'],
            ['fs/readdir.c', 'fs/ext2/dir.c'],
            [],
            ['fs/mount.h', 'fs/pnode.c', 'fs/proc_namespace.c'],
            ['fs/devpts/'],
            ['fs/bad_inode.c', 'fs/eventpoll.c', 'fs/iomap.c', 'fs/locks.c', 'fs/select.c', 'fs/signalfd.c', 
'fs/userfaultfd.c', 'fs/dlm/', 'security/'],
            [],
            ['fs/9p/', 'fs/afs/', 'fs/cifs/', 'fs/configfs/', 'fs/debugfs/', 'fs/ecryptfs/', 'fs/fuse/'],
            ['fs/namei.c', 'fs/namespace.c', 'fs/ext2/namei.c'],
            ['fs/dax.c', 'fs/posix_acl.c', 'fs/ext2/acl.c', 'fs/ext2/acl.h'],
            ['fs/coredump.c'],
            ['fs/nilfs2/']]

