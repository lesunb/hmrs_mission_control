#!/bin/bash
SCRIPT="sudo apt-get update && sudo apt-get upgrade -y"
USERNAME="labpos"
HOSTS="lap-01 lap-02 lap-03 lap-04 lap-05 lap-06"
for HOSTNAME in ${HOSTS} ; do
    ssh  -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "${SCRIPT}" &
done
