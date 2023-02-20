***Study***

For our study of the bug cases please refer to https://github.com/data-storage-lab/BugBench/tree/main/ConfDBugStudy}

***Experimental results from the 6 plugins** 

Number of states don't represent the number of issues. One configuration state may trigger different issues

**Plugin#1: ConfD-specCk (Documentation Issue)**

**Ext4**

1. cluster size max value
2. lazy_init_itable enable value
3. flex_bg max value
4. flex_bg min value
5. inode_ratio max value
6. num_inodes min value
7. lazy_itable_init enable value
9. resize_inode and meta_bg dependency
10. 64bit and extents dependency
11. clustersize and block size dependency
12. size from resize2fs and 64bit from mke2fs dependency
13. force from resize2fs and bigalloc from mke2fs dependency


**XFS**

1. xfs mininum file system size
2. sunit and sw dependency
3. blocksize and crc dependency
4. data sw and data su dependency

**Plugin#2: ConfD-handlingCk (Bad reaction)**

**Ext4**

*Early Termination*

1. mke2fs -O fast_commit,resz_inode 
2. mke2fs -C 512M -O bigalloc
3. mke2fs -C 257M -O bigalloc
4. mke2fs -O ^sparse_super
5. mke2fs -g 9000 

*Functional Failure*
1. mke2fs -E offset=10
2. mke2fs -E desc_size=1

*Silent Violation*
1. mke2fs -E encoding=utf8 -O ^casefold
2. mke2fs -E resize=10000000 -O ^resize_inode
3. mke2fs -J size=50 -O ^has_journal
4. mke2fs -N 1

*Partial Report*
1. mke2fs -O meta_bg,^sparse_super
2. mke2fs -O bigalloc,^extents

**XFS**

*Silent Violation*
1. mkfs.xfs -n ftype=0 -m crc=1

*Partial Report*
1. mkfs.xfs -l sunit=4K,su=4K
2. mkfs.xfs -l su=4K,sunit=4K
3. mkfs.xfs -d su=1000

**Plugin#3: ConfD-rfsck**
1. mke2fs -t ext4 -O resize_inode,sparse_super
2. mke2fs -t ext4 -G 16 -O flex_bg
3. mke2fs -t ext4 -C 32K -O bigalloc,extents
4. mke2fs -t ext4 -I 128 -r 0
5. mke2fs -t ext4 -I 128 -r 1
6. mke2fs -t ext4 -I 256 -r 0
7. mke2fs -t ext4 -I 128 -i 1024
8. mke2fs -t ext4 -I 256 -i 2048
9. mke2fs -t ext4 -C 16K -i 32K -O bigalloc,extents,64bit
10. mke2fs -t ext4 -O resize_inode,sparse_super
11. mke2fs -t ext4 -C 16K -i 32K -I 128 -r 1 -O bigalloc,extents,64bit
12. mke2fs -t ext4 -G 16 -N 8000 -O flex_bg
13. mke2fs -t ext4 -b 1024 -i 1024 -N 8192 -O ^64bit
14. mke2fs -t ext4 -b 2048 -i 1024 -N 8192 -O 64bit
15. mke2fs -t ext4 -O ea_inode
16. mke2fs -t ext4 -O project
17. mke2fs -t ext4 -O casefold
18. mke2fs -t ext4 -O uninit_bg
19. mke2fs -t ext4 -O sparse_super2
20. mke2fs -t ext4 -E encoding=utf8-12.1 -O casefold
21. mke2fs -t ext4 -E encoding=utf8 -O casefold

**Plugin#4: ConfD-gt-hydra**
1. mke2fs -F -I 128 -i 1024
2. mke2fs -b 1024 -I 256 -O inline_data
3. mke2fs -b 1024 -i 1024 -N 8192 -O ^64bit

**Plugin#5: ConfD-xfstests (Test case failure)**

**Ext4**
1. mke2fs -O bigalloc,extents,64bit
2. mke2fs -O quota

**XFS**
1. mkfs.xfs -d su=XXX,sw=XXX
2. mkfs.xfs -m crc=0 ; mount -o usrquota,grpquota,prjquota
3. mkfs.xfs crc=0; xfs_io -c cowextsize=1048576

**Plugin#6: ConfD-e2fsprogs (Test case failure)**
1. mke2fs -O bigalloc,extents,64bit; resize2fs -f 




