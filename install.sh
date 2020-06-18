#!/bin/bash

basepfad="/opt/smarthome";

if ! [ -d "$basepath" ];then

echo "update"

else
sudo apt-get update
sudo apt-get install python3 python3-pip git -y

sudo pip3 install virtualenv


sudo mkdir /opt/smarthome

sudo chown $(id -u):$(id -g) /opt/smarthome

cd /opt

git clone --branch v0.0-beta https://github.com/fholler0371/smarthome.git

cd /opt/smarthome

virtualenv env

fi
ls -l /opt/smarthome



