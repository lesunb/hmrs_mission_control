cp azuervps_key.pem ~/.ssh/remotes/azuervps_key.pem 

cd labtunnel
./install.sh

# append configs
cat ./.ssh/config >> ~/.ssh/config

# test/debug
# ssh labaccessvpstunnel
#systemctl --user start labtunnel@labaccessvpstunnel
#systemctl --user status labtunnel@labaccessvpstunnel
#systemctl --user stop labtunnel@labaccessvpstunnel



