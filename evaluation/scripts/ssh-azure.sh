#!/bin/sh

#ssh -i /Users/grodrigues/dev/hmrs_mission_control/scripts/ssh-azure.pem azureuser@20.195.163.129
# ssh -i /home/gastd/Downloads/aws_sim.pem ubuntu@ec2-18-229-137-44.sa-east-1.compute.amazonaws.com 'tar -czf - /home/ubuntu/git/morse_simulation/log' | tar -xzf -

ssh -i /Users/grodrigues/dev/hmrs_mission_control/scripts/ssh-azure.pem azureuser@20.195.163.129 'tar -czf - /home/azureuser/git/morse_simulation/log/*.log' | tar -xzf -

# scp -i /home/gastd/Downloads/ssh-azure.pem azureuser@20.195.163.129:/home/azureuser/git/morse_simulation/log /home/gastd/
