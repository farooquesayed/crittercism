#!/bin/bash

#prompt password
sudo -p "Enter password:" whoami 1>/dev/null && {sudo whoami;sudo whoami; whoami; sudo -l}

#check for pip
if ! type "pip" > /dev/null; then
    echo "pip not installed. Installing pip..."
    sudo easy_install pip
    echo "pip installation complete."
fi

#manage dependencies with pip
echo "getting packages..."
sudo pip install logger
sudo pip install nose
sudo pip install selenium
sudo pip install setuptools
sudo pip install unittest2
sudo pip install wsgiref
sudo pip install httplib2
sudo pip install requests
echo "installation completed"