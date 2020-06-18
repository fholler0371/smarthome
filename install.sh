#!/bin/bash

dir="/opt"
basepath="$dir/smarthome";

if [ -d "$basepath" ];then

cd $basepath/tmp
git clone https://github.com/fholler0371/smarthome.git
echo "update"

else

sudo apt-get update
sudo apt-get install python3 python3-pip git -y
sudo pip3 install virtualenv
sudo mkdir $basepath 
sudo chown $(id -u):$(id -g) $basepath
cd $dir
git clone https://github.com/fholler0371/smarthome.git
cd $basepath
virtualenv env

fi

cd $basepath
env/bin/pip install -r requirements.txt
file="$basepath/smarthome.py"
sed -i -e "1d" $file
sed  -i "1i #!$basepath/env/bin/python" $file
sudo chown -R $(id -u):$(id -g) $basepath
sudo chmod +x $file
$file install
$file restart

ls -l $basepath



