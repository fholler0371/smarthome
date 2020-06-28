#!/bin/bash
#
# Sript zur Installation von smarthome
#
###########################################

# Parentverzeichnis zur Installation
dir="/opt"

#Verzeichnis in dem alle Koponenten installiert werden
basepath="$dir/smarthome";

#check ob bereits eine Installation vorliegt
if [ -d "$basepath" ];then
# Update
#
#Download des Programms ins tmp Verzeichnis und anschliessend verschieben ins 
#Installationsverzeichnis
cd $basepath/tmp
rm -R --force smarthome
git clone https://github.com/fholler0371/smarthome.git
cd $basepath
cp -R tmp/smarthome/* ./
rm -R --force tmp/smarthome


else
# Neu Installation
#
sudo apt-get update
sudo apt-get install python3 python3-pip git -y
# Libary fuer virtuelles Verzeichnis
sudo pip3 install virtualenv
# Erzeugen des Basisverzeichnis fuer aktuellen Nutzer
sudo mkdir $basepath
sudo chown $(id -u):$(id -g) $basepath
# Downlad des Programms
cd $dir
git clone https://github.com/fholler0371/smarthome.git
cd $basepath
# Erstellen des Virtuellen Enviroments
virtualenv env
fi

# Laden der notwendigen Python-Bibliotheken
cd $basepath
env/bin/pip install -r requirements.txt

# anpassen des Interpreters in client.py und setzten der Rechte
file="$basepath/client.py"
sed -i -e "1d" $file
sed  -i "1i #!$basepath/env/bin/python" $file
sudo chmod +x $file

# anpassen des Interpreters in smarthome.py und setzen der Rechte
file="$basepath/smarthome.py"
sed -i -e "1d" $file
sed  -i "1i #!$basepath/env/bin/python" $file
sudo chown -R $(id -u):$(id -g) $basepath
sudo chmod +x $file

# Installation und starten der neuen Version
$file install
$file restart

cd $basepath
bash get_js.sh
