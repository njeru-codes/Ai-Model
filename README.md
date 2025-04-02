Understood! Here's a step-by-step guide using only commands to increase the size of the root partition (/) on your sdb disk, assuming you have unallocated space available. We will use fdisk, resize2fs, and parted in this process.
Prerequisites:

    You must boot from a Live USB/CD because the root partition (/) cannot be resized while it’s mounted.

    This guide assumes the root partition is /dev/sdb2 and you have unallocated space on the disk.

Steps:

    Boot from Live USB/CD: Boot your Kali Linux live USB/CD.

    Open a terminal and check your partitions using lsblk:

lsblk

This should show your disk structure, and you'll see sdb2 as your root partition.

Use fdisk to delete and recreate the root partition (/dev/sdb2):

    Start fdisk on /dev/sdb:

    sudo fdisk /dev/sdb

    First, note the starting sector of /dev/sdb2. To do this, type p to print the partition table, then note down the "Start" sector of /dev/sdb2.

Example output:

Device     Start      End  Sectors  Size Type
/dev/sdb1   2048    149503   147456  72M EFI System
/dev/sdb2  149504  78131200  77981760  37.1G Linux filesystem
/dev/sdb3 78131201  83880959   5753760   2.7G Linux swap

In this example, the start sector for /dev/sdb2 is 149504.

Delete and recreate the root partition (/dev/sdb2):

    Type d to delete the partition.

    Enter 2 (the number for /dev/sdb2) when prompted.

    Then, type n to create a new partition.

    Choose 2 (the same partition number).

    Set the start sector to the same value as it was before (e.g., 149504).

    For the "End" sector, just press Enter to use the default value, which should use the unallocated space and extend the partition.

Write the changes:

After creating the new partition with the extended size, type w to write the changes.

w

Resize the filesystem:

Now that the partition is extended, we need to resize the filesystem to fill the new partition size. Since your root partition is likely formatted with ext4, use resize2fs to resize the filesystem:

sudo resize2fs /dev/sdb2

This will expand the filesystem to use the full size of the partition.

Check the partition and filesystem:

After resizing, you can check that everything worked properly by running:

sudo lsblk

You should see that /dev/sdb2 now occupies the full available space.

Reboot:

Reboot your system to the regular environment:

    sudo reboot

Final Notes:

    Backup: Always backup your data before making changes to partitions and filesystems.

    Swap Partition: If you need more space, you can resize or remove the swap partition (/dev/sdb3) and follow similar steps.

Let me know if you run into any issues or need further clarification on any of the steps!
