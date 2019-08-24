#! /bin/sh

qemu-system-x86_64 \
-m 128M \
-kernel ./bzImage \
-initrd  ./rootfs.cpio \
-append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 kaslr" \
-monitor /dev/null \
-nographic 2>/dev/null \
-smp cores=2,threads=1 \
-cpu kvm64,+smep 
