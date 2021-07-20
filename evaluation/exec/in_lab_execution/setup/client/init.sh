ssh-copy-id -i $HOME/.ssh/id_rsa.pub labaccessvps
cat ./.ssh/config-les >> ~/.ssh/config
ssh-copy-id -i $HOME/.ssh/id_rsa.pub labvirtual
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-01
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-02
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-03
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-04
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-05
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-06
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-07
ssh-copy-id -i $HOME/.ssh/id_rsa.pub les-08


cat ./.ssh/config-labpos >> ~/.ssh/config
ssh-copy-id -i $HOME/.ssh/id_rsa.pub labvirtual2
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-01
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-02
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-03
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-04
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-05
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-06
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-07
ssh-copy-id -i $HOME/.ssh/id_rsa.pub lap-08

