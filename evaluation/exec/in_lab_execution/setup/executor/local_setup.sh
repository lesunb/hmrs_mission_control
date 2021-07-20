set LAB_ADDRESS_BASE=164.41.76
set LABACCESS_ADDR=$LAB_ADDRESS_BASE.21
set LABACCESS_SSH=labpos@LABACCESS_ADDR


sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
#sudo adduser lesunb
#sudo usermod -aG sudo lesunb
#su - lesunb
set my_ip4=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
set ADD_TO_HOSTS_SCRIPT="echo '$hostname $LAB_ADDRESS_BASE' >> /etc/hosts'"
ssh $LABACCESS_SSH ""

#sudo visudo

# no passw for sudo 
# labpos ALL=(ALL) NOPASSWD:ALL

