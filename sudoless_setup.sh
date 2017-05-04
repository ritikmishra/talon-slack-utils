#!/bin/sh
curl https://nodejs.org/dist/v6.10.3/node-v6.10.3-darwin-x64.tar.gz >> $HOME/node-v6.10.3-darwin-x64.tar.gz

mkdir $HOME/node
tar xvf $HOME/node-v6.10.3-darwin-x64.tar.gz -C $HOME/node

mkdir ~/python_packages

echo "export PATH=\"$HOME/python_packages:$HOME/node/node-v6.10.3-darwin-x64/bin:$PATH\"\nexport PYTHONPATH=$HOME/python_packages" >> ~/.bash_profile

export PYTHONPATH=$HOME/python_packages

easy_install --install-dir=$HOME/python_packages pip
easy_install --install-dir=$HOME/python_packages wheel

pip install -r requirements.txt

source ~/.bash_profile
