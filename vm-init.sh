#!/bin/sh

# Update packages
sudo apt-get -y update
sudo apt-get -y upgrade

# Add ericsson to /etc/hosts
IP="129.192.68.4"
HOSTNAME="xerces.ericsson.net"

if [ -n "$(grep $HOSTNAME /etc/hosts)" ]
then
        echo "$HOSTNAME already added in /etc/hosts"
else
        sed -i "2i$IP $HOSTNAME" /etc/hosts
fi
