#!/bin/bash
SCRIPT="sudo service gdm stop && sudo init 3 && who -r"
USERNAME="lesunb"
HOSTS="les-01 les-02 les-03 les-04 les-05 les-06 les-07 les-08"
for HOSTNAME in ${HOSTS} ; do
    ssh  -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "${SCRIPT}"
done
