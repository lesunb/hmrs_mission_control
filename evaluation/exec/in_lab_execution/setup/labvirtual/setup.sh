sudo sudo cat ./hosts >> /etc/hosts

#ping lab-01

chmod +x ./set_autossh_tunnel.sh
./set_autossh_tunnel.sh

chmod +x ./configure_clients.sh
./configure_clients.sh