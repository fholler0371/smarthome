#!/bin/bash

dir="/opt"
basepath="$dir/smarthome";

if [ -d "$basepath" ];then

echo "update"

else
sudo apt-get update
sudo apt-get install python3 python3-pip git -y

sudo pip3 install virtualenv


sudo mkdir $basepath 

sudo chown $(id -u):$(id -g) $basepath

cd $dir

git clone --branch v0.0-beta https://github.com/fholler0371/smarthome.git

cd $basepath

virtualenv env

fi

file="$basepath/smarthome.py"

echo $file

sed -i -e "1d" $file

sed  -i "1i #!$basepath/env/bin/python" $file

sudo chown -R $(id -u):$(id -g) $basepath
sudo chmod +x $file

$file install
$file restart

ls -l $basepath



