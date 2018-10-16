#!/bin/bash

set -x
sudo install -m 755 -o root -g root /tmp/wattime.sh /usr/bin
sudo install -m 600 -o root -g root /tmp/cronroot /var/spool/cron/root
set +x
exit 0
