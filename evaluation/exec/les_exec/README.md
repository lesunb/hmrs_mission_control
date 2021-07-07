

# Overview

In order to gain acess to machines in the lab we have public machine, labacessvps, with an updated dns name. 
And a labvirtual that creates a persistent ssh tunnel to the labacessvps. The labvirtual also have the names for the other machines in the network of the university. Clients, the machines of researchers, outside of the university access the workstations by ssh through jumps into the labacessvps, and labvirtual. Due to facilities in configuration in .ssh/config the access can be seamless for ssh, and scp. 


# SETUP client (machine used by the researcher)

Executed after labaccessvps, labvirtual, and each workstations are configured.

## setup access with pem file

'''

1. append client/.ssh/config content to your ~/.ssh/config

'''
cat client/.ssh/config >> ~/.ssh/config
'''

2. Put the key file to the path pointed by .ssh/config

'''
cp labaccessvps.pem ~/.ssh/remotes/labaccessvps.pem
'''

3. Add the pub key of your machine to the labaccessvps, labvirtual and each workstations

'''
./client/init.sh
'''

## Execute remote commands
'''
ssh les-01
'''

## Copying files from and to remote

'''
scp les-01:~/.profile .
scp test.txt les-01:~
'''

## test access to labaccess (cloud machine)
'''
ssh labaccessvps
exit
'''

## test access to labvirtual (gate machine in the laboratory)
'''
ssh labvirtual
exit
'''


## SETUP labvirtual server

TODO

## SETUP labaccessvps

TODO




