mv ./home/ubuntu/git/morse_simulation/log old
ssh -i ssh-azure.pem ubuntu@ec2-18-229-137-44.sa-east-1.compute.amazonaws.com 'tar -czf - /home/ubuntu/git/morse_simulation/log' | tar -xzf -