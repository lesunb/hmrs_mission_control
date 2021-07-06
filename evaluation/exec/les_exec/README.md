# SSH through noes

ssh -J azurevps lesunb@les-05

# SCP
SCP doesn't have the -J argument, but it does allow -o, so this works:

scp -o ProxyJump=remotevps file.txt you@node2:~


# SETUP client (machine used by the operator)

## setup access with pem file

'''
cp azuervps.pem ~/.ssh/remotes/azuervps.pem
'''

then append client/.ssh/config content to your ~/.ssh/config

'''
cat client/.ssh/config >> ~/.ssh/config
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

## test access to other lab machines
'''
ssh lab1
exit
'''



# SETUP

# SETUP lab_virtual server

1. gen key
'''
ssh-keygen -t rsa
'''

2. 
\