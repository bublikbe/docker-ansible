#!/bin/bash
for i in $(seq 1 30); do
    if [ -f /keys/master.pub ]; then
        cp /keys/master.pub /root/.ssh/authorized_keys
        chmod 600 /root/.ssh/authorized_keys
        break
    fi
    sleep 1
done

exec /usr/sbin/sshd -D
