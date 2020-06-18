import argparse
import subprocess
import os

SCRIPT = '''
[Unit]
Description=file
After=network.target

[Service]
ExecStart=path/file.py
WorkingDirectory=path
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
'''

def run(sh):
    parser = argparse.ArgumentParser(description='Smarthome Dienstoptionen')
    parser.add_argument('command', type=str, choices=['install', 'uninstall', 'start', 'stop', 'restart', 'status'])
    args = parser.parse_args()
    if args.command == 'install':
        global SCRIPT
        script = SCRIPT.replace('file', sh.basename).replace('path', sh.basepath)
        f = open(sh.basepath + '/tmp/service', 'w+')
        f.write(script)
        f.close()
        subprocess.run(('sudo cp ' + sh.basepath + '/tmp/service /etc/systemd/system/' + sh.basename + '.service').split(' '))
        os.remove(sh.basepath + '/tmp/service')
        subprocess.run(('sudo systemctl enable ' + sh.basename + '.service').split(' '))
        subprocess.run(('sudo systemctl start ' + sh.basename + '.service').split(' '))
    elif args.command == 'uninstall':
        subprocess.run(('sudo systemctl stop ' + sh.basename + '.service').split(' '))
        subprocess.run(('sudo systemctl disable ' + sh.basename + '.service').split(' '))
        subprocess.run(('sudo rm /etc/systemd/system/' + sh.basename + '.service').split(' '))
    elif args.command == 'start':
        subprocess.run(('sudo systemctl start ' + sh.basename + '.service').split(' '))
    elif args.command == 'stop':
        subprocess.run(('sudo systemctl stop ' + sh.basename + '.service').split(' '))
    elif args.command == 'restart':
        subprocess.run(('sudo systemctl start ' + sh.basename + '.service').split(' '))
        subprocess.run(('sudo systemctl stop ' + sh.basename + '.service').split(' '))
    elif args.command == 'status':
        result = subprocess.run(('sudo systemctl status ' + sh.basename + '.service').split(' '), capture_output=True)
        for line in result.stdout.decode().split('\n'):
            print(line)
        for line in result.stderr.decode().split('\n'):
            print(line)
