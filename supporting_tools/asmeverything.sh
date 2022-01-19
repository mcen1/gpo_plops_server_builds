#!/bin/bash
# deprecated
echo ALL UNFORMATTED DISKS WILL BECOME ASM DISKS! GOOD LUCK!

for DISK2FORMAT in $(lsblk -r --output NAME,MOUNTPOINT | awk -F \/ '/sd/ { dsk=substr($1,1,3);dsks[dsk]+=1 } END { for ( i in dsks ) { if (dsks[i]==1) print i } }'); do
echo formatting /dev/$DISK2FORMAT ...
(
echo n # Add a new partition
echo p # Primary partition
echo 1 # Partition number
echo   # First sector (Accept default: 1)
echo   # Last sector (Accept default: varies)
echo w # Write changes
) | sudo fdisk /dev/$DISK2FORMAT
done

