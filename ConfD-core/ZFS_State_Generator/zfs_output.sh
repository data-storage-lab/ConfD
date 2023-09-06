#!/bin/bash

zfs create -b 512 -o copies=1 -V 1G /zpool/volume1
zfs create -b 512 -V 1G /zpool/volume2
zfs create -b 512 -o copies=3 -V 1G /zpool/volume3
zfs create -b 512 -o compression=off -o copies=1 -V 1G /zpool/volume4
zfs create -b 512 -o compression=off -V 1G /zpool/volume5
zfs create -b 512 -o compression=off -o copies=3 -V 1G /zpool/volume6
zfs create -b 512 -o checksum=off -o copies=1 -V 1G /zpool/volume7
zfs create -b 512 -o checksum=off -V 1G /zpool/volume8
zfs create -b 512 -o checksum=off -o copies=3 -V 1G /zpool/volume9
zfs create -b 512 -o checksum=off -o compression=off -o copies=1 -V 1G /zpool/volume10
zfs create -b 512 -o checksum=off -o compression=off -V 1G /zpool/volume11
zfs create -b 512 -o checksum=off -o compression=off -o copies=3 -V 1G /zpool/volume12
zfs create -b 1024 -o copies=1 -V 1G /zpool/volume13
zfs create -b 1024 -V 1G /zpool/volume14
zfs create -b 1024 -o copies=3 -V 1G /zpool/volume15
zfs create -b 1024 -o compression=off -o copies=1 -V 1G /zpool/volume16
zfs create -b 1024 -o compression=off -V 1G /zpool/volume17
zfs create -b 1024 -o compression=off -o copies=3 -V 1G /zpool/volume18
zfs create -b 1024 -o checksum=off -o copies=1 -V 1G /zpool/volume19
zfs create -b 1024 -o checksum=off -V 1G /zpool/volume20
zfs create -b 1024 -o checksum=off -o copies=3 -V 1G /zpool/volume21
zfs create -b 1024 -o checksum=off -o compression=off -o copies=1 -V 1G /zpool/volume22
zfs create -b 1024 -o checksum=off -o compression=off -V 1G /zpool/volume23
zfs create -b 1024 -o checksum=off -o compression=off -o copies=3 -V 1G /zpool/volume24
zfs create -b 2048 -o copies=1 -V 1G /zpool/volume25
zfs create -b 2048 -V 1G /zpool/volume26
zfs create -b 2048 -o copies=3 -V 1G /zpool/volume27
zfs create -b 2048 -o compression=off -o copies=1 -V 1G /zpool/volume28
zfs create -b 2048 -o compression=off -V 1G /zpool/volume29
zfs create -b 2048 -o compression=off -o copies=3 -V 1G /zpool/volume30
zfs create -b 2048 -o checksum=off -o copies=1 -V 1G /zpool/volume31
zfs create -b 2048 -o checksum=off -V 1G /zpool/volume32
zfs create -b 2048 -o checksum=off -o copies=3 -V 1G /zpool/volume33
zfs create -b 2048 -o checksum=off -o compression=off -o copies=1 -V 1G /zpool/volume34
zfs create -b 2048 -o checksum=off -o compression=off -V 1G /zpool/volume35
zfs create -b 2048 -o checksum=off -o compression=off -o copies=3 -V 1G /zpool/volume36
zfs create -b 4096 -o copies=1 -V 1G /zpool/volume37
zfs create -b 4096 -V 1G /zpool/volume38
zfs create -b 4096 -o copies=3 -V 1G /zpool/volume39
zfs create -b 4096 -o compression=off -o copies=1 -V 1G /zpool/volume40
zfs create -b 4096 -o compression=off -V 1G /zpool/volume41
zfs create -b 4096 -o compression=off -o copies=3 -V 1G /zpool/volume42
zfs create -b 4096 -o checksum=off -o copies=1 -V 1G /zpool/volume43
zfs create -b 4096 -o checksum=off -V 1G /zpool/volume44
zfs create -b 4096 -o checksum=off -o copies=3 -V 1G /zpool/volume45
zfs create -b 4096 -o checksum=off -o compression=off -o copies=1 -V 1G /zpool/volume46
zfs create -b 4096 -o checksum=off -o compression=off -V 1G /zpool/volume47
zfs create -b 4096 -o checksum=off -o compression=off -o copies=3 -V 1G /zpool/volume48
zfs create -b 8192 -o copies=1 -V 1G /zpool/volume49
zfs create -b 8192 -V 1G /zpool/volume50
zfs create -b 8192 -o copies=3 -V 1G /zpool/volume51
zfs create -b 8192 -o compression=off -o copies=1 -V 1G /zpool/volume52
zfs create -b 8192 -o compression=off -V 1G /zpool/volume53
zfs create -b 8192 -o compression=off -o copies=3 -V 1G /zpool/volume54
zfs create -b 8192 -o checksum=off -o copies=1 -V 1G /zpool/volume55
zfs create -b 8192 -o checksum=off -V 1G /zpool/volume56
zfs create -b 8192 -o checksum=off -o copies=3 -V 1G /zpool/volume57
zfs create -b 8192 -o checksum=off -o compression=off -o copies=1 -V 1G /zpool/volume58
zfs create -b 8192 -o checksum=off -o compression=off -V 1G /zpool/volume59
zfs create -b 8192 -o checksum=off -o compression=off -o copies=3 -V 1G /zpool/volume60
zfs create -b 16384 -o copies=1 -V 1G /zpool/volume61
zfs create -b 16384 -V 1G /zpool/volume62
zfs create -b 16384 -o copies=3 -V 1G /zpool/volume63
zfs create -b 16384 -o compression=off -o copies=1 -V 1G /zpool/volume64
zfs create -b 16384 -o compression=off -V 1G /zpool/volume65
zfs create -b 16384 -o compression=off -o copies=3 -V 1G /zpool/volume66
zfs create -b 16384 -o checksum=off -o copies=1 -V 1G /zpool/volume67
zfs create -b 16384 -o checksum=off -V 1G /zpool/volume68
zfs create -b 16384 -o checksum=off -o copies=3 -V 1G /zpool/volume69
zfs create -b 16384 -o checksum=off -o compression=off -o copies=1 -V 1G /zpool/volume70
zfs create -b 16384 -o checksum=off -o compression=off -V 1G /zpool/volume71
zfs create -b 16384 -o checksum=off -o compression=off -o copies=3 -V 1G /zpool/volume72
zfs create -b 32768 -o copies=1 -V 1G /zpool/volume73
zfs create -b 32768 -V 1G /zpool/volume74
zfs create -b 32768 -o copies=3 -V 1G /zpool/volume75
zfs create -b 32768 -o compression=off -o copies=1 -V 1G /zpool/volume76
zfs create -b 32768 -o compression=off -V 1G /zpool/volume77
zfs create -b 32768 -o compression=off -o copies=3 -V 1G /zpool/volume78
zfs create -b 32768 -o checksum=off -o copies=1 -V 1G /zpool/volume79
zfs create -b 32768 -o checksum=off -V 1G /zpool/volume80
zfs create -b 32768 -o checksum=off -o copies=3 -V 1G /zpool/volume81
zfs create -b 32768 -o checksum=off -o compression=off -o copies=1 -V 1G /zpool/volume82
zfs create -b 32768 -o checksum=off -o compression=off -V 1G /zpool/volume83
zfs create -b 32768 -o checksum=off -o compression=off -o copies=3 -V 1G /zpool/volume84
zfs create -o recordsize=512 -o copies=1 /zpool/block1
zfs create -o recordsize=512 /zpool/block2
zfs create -o recordsize=512 -o copies=3 /zpool/block3
zfs create -o recordsize=512 -o compression=off -o copies=1 /zpool/block4
zfs create -o recordsize=512 -o compression=off /zpool/block5
zfs create -o recordsize=512 -o compression=off -o copies=3 /zpool/block6
zfs create -o recordsize=512 -o checksum=off -o copies=1 /zpool/block7
zfs create -o recordsize=512 -o checksum=off /zpool/block8
zfs create -o recordsize=512 -o checksum=off -o copies=3 /zpool/block9
zfs create -o recordsize=512 -o checksum=off -o compression=off -o copies=1 /zpool/block10
zfs create -o recordsize=512 -o checksum=off -o compression=off /zpool/block11
zfs create -o recordsize=512 -o checksum=off -o compression=off -o copies=3 /zpool/block12
zfs create -o recordsize=1024 -o copies=1 /zpool/block13
zfs create -o recordsize=1024 /zpool/block14
zfs create -o recordsize=1024 -o copies=3 /zpool/block15
zfs create -o recordsize=1024 -o compression=off -o copies=1 /zpool/block16
zfs create -o recordsize=1024 -o compression=off /zpool/block17
zfs create -o recordsize=1024 -o compression=off -o copies=3 /zpool/block18
zfs create -o recordsize=1024 -o checksum=off -o copies=1 /zpool/block19
zfs create -o recordsize=1024 -o checksum=off /zpool/block20
zfs create -o recordsize=1024 -o checksum=off -o copies=3 /zpool/block21
zfs create -o recordsize=1024 -o checksum=off -o compression=off -o copies=1 /zpool/block22
zfs create -o recordsize=1024 -o checksum=off -o compression=off /zpool/block23
zfs create -o recordsize=1024 -o checksum=off -o compression=off -o copies=3 /zpool/block24
zfs create -o recordsize=2048 -o copies=1 /zpool/block25
zfs create -o recordsize=2048 /zpool/block26
zfs create -o recordsize=2048 -o copies=3 /zpool/block27
zfs create -o recordsize=2048 -o compression=off -o copies=1 /zpool/block28
zfs create -o recordsize=2048 -o compression=off /zpool/block29
zfs create -o recordsize=2048 -o compression=off -o copies=3 /zpool/block30
zfs create -o recordsize=2048 -o checksum=off -o copies=1 /zpool/block31
zfs create -o recordsize=2048 -o checksum=off /zpool/block32
zfs create -o recordsize=2048 -o checksum=off -o copies=3 /zpool/block33
zfs create -o recordsize=2048 -o checksum=off -o compression=off -o copies=1 /zpool/block34
zfs create -o recordsize=2048 -o checksum=off -o compression=off /zpool/block35
zfs create -o recordsize=2048 -o checksum=off -o compression=off -o copies=3 /zpool/block36
zfs create -o recordsize=4096 -o copies=1 /zpool/block37
zfs create -o recordsize=4096 /zpool/block38
zfs create -o recordsize=4096 -o copies=3 /zpool/block39
zfs create -o recordsize=4096 -o compression=off -o copies=1 /zpool/block40
zfs create -o recordsize=4096 -o compression=off /zpool/block41
zfs create -o recordsize=4096 -o compression=off -o copies=3 /zpool/block42
zfs create -o recordsize=4096 -o checksum=off -o copies=1 /zpool/block43
zfs create -o recordsize=4096 -o checksum=off /zpool/block44
zfs create -o recordsize=4096 -o checksum=off -o copies=3 /zpool/block45
zfs create -o recordsize=4096 -o checksum=off -o compression=off -o copies=1 /zpool/block46
zfs create -o recordsize=4096 -o checksum=off -o compression=off /zpool/block47
zfs create -o recordsize=4096 -o checksum=off -o compression=off -o copies=3 /zpool/block48
zfs create -o copies=1 /zpool/block49
zfs create /zpool/block50
zfs create -o copies=3 /zpool/block51
zfs create -o compression=off -o copies=1 /zpool/block52
zfs create -o compression=off /zpool/block53
zfs create -o compression=off -o copies=3 /zpool/block54
zfs create -o checksum=off -o copies=1 /zpool/block55
zfs create -o checksum=off /zpool/block56
zfs create -o checksum=off -o copies=3 /zpool/block57
zfs create -o checksum=off -o compression=off -o copies=1 /zpool/block58
zfs create -o checksum=off -o compression=off /zpool/block59
zfs create -o checksum=off -o compression=off -o copies=3 /zpool/block60
zfs create -o recordsize=16384 -o copies=1 /zpool/block61
zfs create -o recordsize=16384 /zpool/block62
zfs create -o recordsize=16384 -o copies=3 /zpool/block63
zfs create -o recordsize=16384 -o compression=off -o copies=1 /zpool/block64
zfs create -o recordsize=16384 -o compression=off /zpool/block65
zfs create -o recordsize=16384 -o compression=off -o copies=3 /zpool/block66
zfs create -o recordsize=16384 -o checksum=off -o copies=1 /zpool/block67
zfs create -o recordsize=16384 -o checksum=off /zpool/block68
zfs create -o recordsize=16384 -o checksum=off -o copies=3 /zpool/block69
zfs create -o recordsize=16384 -o checksum=off -o compression=off -o copies=1 /zpool/block70
zfs create -o recordsize=16384 -o checksum=off -o compression=off /zpool/block71
zfs create -o recordsize=16384 -o checksum=off -o compression=off -o copies=3 /zpool/block72
zfs create -o recordsize=32768 -o copies=1 /zpool/block73
zfs create -o recordsize=32768 /zpool/block74
zfs create -o recordsize=32768 -o copies=3 /zpool/block75
zfs create -o recordsize=32768 -o compression=off -o copies=1 /zpool/block76
zfs create -o recordsize=32768 -o compression=off /zpool/block77
zfs create -o recordsize=32768 -o compression=off -o copies=3 /zpool/block78
zfs create -o recordsize=32768 -o checksum=off -o copies=1 /zpool/block79
zfs create -o recordsize=32768 -o checksum=off /zpool/block80
zfs create -o recordsize=32768 -o checksum=off -o copies=3 /zpool/block81
zfs create -o recordsize=32768 -o checksum=off -o compression=off -o copies=1 /zpool/block82
zfs create -o recordsize=32768 -o checksum=off -o compression=off /zpool/block83
zfs create -o recordsize=32768 -o checksum=off -o compression=off -o copies=3 /zpool/block84
