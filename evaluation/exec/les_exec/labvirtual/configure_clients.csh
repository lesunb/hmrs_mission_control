#!/bin/csh
echo "Setting name servers...."
set LES_VIRTUAL_ADDR=164.41.75.165
ssh-keygen -t rsa
foreach i ( 1 2 3 )
    ssh-copy-id -i $HOME/.ssh/id_rsa.pub lesunb@les-0$i.lesunb
end