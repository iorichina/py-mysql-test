import pymysql
import time
import sys
from sys import argv
import json
from scp import SCPClient
import paramiko

print "current system timestamp:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

filename = "args.ssh-connect-test.json"
if len(argv) > 6 or len(argv) < 5:
    print "usage: "
    print "]$ python proxy-ssh-connect-test.py host      port   user    passwd  [ssh-args-file(default 'args.ssh-connect-test.json')]"
    print "]$ python proxy-ssh-connect-test.py 192.0.0.9 32200  iori    iori"
    print "]$ python proxy-ssh-connect-test.py p.iori.cc 32200  iori    iori    args.json"
    sys.exit()

if len(argv) > 5:
    filename = argv[5]

proxystr = "".join(("[", argv[1], ":", argv[2], "]"))

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(argv[1], int(argv[2]), argv[3], argv[4], timeout=5)

# TODO:test python version
stdin, stdout, stderr = ssh.exec_command('python -V')
print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())

# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())

# upload file name
_dir_name = "py-mysql-test"
_file_names = {"connect-test.py":False, "ssh-connect-test.py":False, "pymysql":True, "paramiko":True, "Crypto":True}

ssh.exec_command('mkdir -p ' + _dir_name)
recursive=False
# upload files
try:
    for f in _file_names.keys():
        scp.put(f, _dir_name, _file_names[f])
finally:
    scp.close()
    pass

test_command = ''.join(('python ssh-connect-test.py ', filename))
stdin, stdout, stderr = ssh.exec_command(test_command)

print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())
