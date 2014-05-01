#!/bin/bash

# The vnc password to use...
VNC_PW="password"
VNC_ROOT="/root/"

# Setup a gnome env
wget "http://mirror.metrocast.net/fedora/epel/6/i386/epel-release-6-8.noarch.rpm" -O "/tmp/epel-release-6-8.noarch.rpm"
rpm -i "/tmp/epel-release-6-8.noarch.rpm"

# Something off in ylinux...
yum -y remove libXfont
yum -y install libXfont

yum -y groupinstall "X Window System"
yum -y groupinstall "Desktop"
yum -y install tigervnc-server tigervnc tigervnc-server-module

# Start it on vnc port 1
echo 'VNCSERVERS="1:root"' >> /etc/sysconfig/vncservers
echo 'VNCSERVERARGS[1]="-geometry 1024x768"' >> /etc/sysconfig/vncservers

# Setup your root password
mkdir -pv $VNC_ROOT/.vnc/
echo "$VNC_PW" | vncpasswd -f > $VNC_ROOT/.vnc/passwd
chmod 600 $VNC_ROOT/.vnc/passwd

# Start it
service vncserver restart
