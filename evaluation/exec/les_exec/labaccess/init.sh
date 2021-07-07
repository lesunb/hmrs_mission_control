sudo useradd labvirtual
sudo usermod -aG sudo labvirtual
su - labvirtual
ssh-keygen -t rsa

ssh-copy-id -i $HOME/.ssh/id_rsa.pub labvirtual