cp labaccessvps_key.pem ~/.ssh/remotes/labaccessvps_key.pem 
chmod 400 ~/.ssh/remotes/labaccessvps_key.pem

# append configs
cat ./.ssh/config >> ~/.ssh/config

# test
#ssh labaccessvps 
cd ./labtunnel/ 
install.sh

# test/debug
# ssh labaccessvpstunnel
#systemctl --user start labtunnel@labaccessvpstunnel
#systemctl --user status labtunnel@labaccessvpstunnel
#systemctl --user stop labtunnel@labaccessvpstunnel


# Automatic start-up of systemd user instances
## otherwise the labtunnel with be only run when labvirtual has an active session
loginctl enable-linger labvirtual 

