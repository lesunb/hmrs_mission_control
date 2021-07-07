#!/bin/bash
SCRIPT="sudo apt-get update && sudo apt-get upgrade"
USERNAME="lesunb"
PASSWORd="lesunb"
HOSTS="labvirtual"
for HOSTNAME in ${HOSTS} ; do
    ssh  -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "${SCRIPT}"
done
