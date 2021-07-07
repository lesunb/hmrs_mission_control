#!/bin/bash

#sudo cat ./hosts >> /etc/hosts

echo "Setting name servers...."
#set LABVIRTUAL_ADDR=164.41.75.165
# ssh-keygen -t rsa
declare -a arr=( 2 3 4 5 6 7 8)
# for i in "${arr[@]}"
# do
#     ssh-copy-id -i $HOME/.ssh/id_rsa.pub lesunb@les-0$i
# done

for i in "${arr[@]}"
do
    ssh lesunb@les-0$i
done