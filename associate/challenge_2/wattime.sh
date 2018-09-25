#!/bin/bash

# I am a horrible bash script that fills your disks with garbage
# but you can't turn me off or fix me for business reasons
# Behold, my tyranny is endless
# muahahahahaaaaaaa!!

dd if=/dev/zero of=/tmp/wattime/$(date "+%s") bs=512 count=2048
date "+%s"
