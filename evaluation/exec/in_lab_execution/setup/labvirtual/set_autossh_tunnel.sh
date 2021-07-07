cp azuervps_key.pem ~/.ssh/remotes/azuervps_key.pem 

cd labtunnel
./install.sh

# Automatic start-up of systemd user instances
## otherwise the labtunnel with be only run when labvirtual has an active session
loginctl enable-linger labvirtual 

# append configs
cat ./.ssh/config >> ~/.ssh/config

# test/debug
# ssh labaccessvpstunnel
#systemctl --user start labtunnel@labaccessvpstunnel
#systemctl --user status labtunnel@labaccessvpstunnel
#systemctl --user stop labtunnel@labaccessvpstunnel



