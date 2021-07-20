#!/bin/bash
SCRIPT='echo "here is "+$HOSTNAME'
USERNAME="labpos"
HOSTS="lap-01 lap-02 lap-03 lap-04 lap-05 lap-06 lap-07"
for HOST in ${HOSTS} ; do
    echo "Hello, ${HOST}!"
    ssh  -o StrictHostKeyChecking=no -l ${USERNAME} ${HOST} "from ${HOST}:"+"${SCRIPT}" &
done


