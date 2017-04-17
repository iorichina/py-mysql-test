import sys
import os

libpath=os.path.join('lib','site-packages')
if os.path.exists(libpath):
    sys.path.append(libpath)
else:
    libpath=os.path.join('lib','python2.6','site-packages')
    if os.path.exists(libpath):
        sys.path.append(libpath)
    else:
        libpath='.'

import pymysql
import time
from sys import argv
import json
from scp import SCPClient
import paramiko

print "current system timestamp:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

defaultfilename = "args.ssh-connect-test.json"
if len(argv) > 6 or len(argv) < 5:
    print "usage: "
    print "]$ python proxy-ssh-connect-test.py host      port   user    passwd  [ssh-args-file('",defaultfilename,"')]"
    print "]$ python proxy-ssh-connect-test.py 192.0.0.9 32200  iori    iori"
    print "]$ python proxy-ssh-connect-test.py p.iori.cc 32200  iori    iori    args.json"
    sys.exit()

filename=defaultfilename
if len(argv) > 5:
    filename = argv[5]

proxystr = "".join(("[", argv[1], ":", argv[2], "]"))

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(argv[1], int(argv[2]), argv[3], argv[4], timeout=5)

# TODO:test python version
stdin, stdout, stderr = ssh.exec_command('python -V')
_stdout = ''.join(stdout.readlines())
_stderr = ''.join(stderr.readlines())
print proxystr, _stdout, _stderr

# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())

_dir_name = "py-mysql-test"
_ssh_test_file_name = "ssh-connect-test.py"
_test_file_name = "connect-test.py"

_do_upload = True

if _do_upload:
    print 'doing upload'
    
    _file_names = {_ssh_test_file_name:False,_test_file_name:False,"scp.py":False,"paramiko":True,"pymysql":True,"cryptography":True,"packaging":True,"asn1crypto":True,"pkg_resources":True,"enum":True,"six.py":False,"pyasn1":True}
    ssh.exec_command('mkdir -p ' + _dir_name)
    # upload files
    try:
        scp.put(filename, _dir_name+"/"+defaultfilename)
        for f in _file_names.keys():
            # TODO test file exists and is updated
            scp.put(f, _dir_name, _file_names[f])
            ssh.exec_command('chmod -R 744 ' + _dir_name + '/' + f)
            pass
    finally:
        scp.close()
        pass

print 'doing ls',_dir_name
test_command = ''.join(('ls ', _dir_name))
stdin, stdout, stderr = ssh.exec_command(test_command)
print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())

file_object = open(filename)
try:
    all_the_text = file_object.read()
    args = json.loads(all_the_text)
except json.ValueError, ve:
    print "args file has not a valid json content"
    sys.exit()
finally:
    file_object.close()

if len(args) < 1:
    print "args file has no content"
    sys.exit()

# loop each ssh server
for arg in args:
    if len(arg) < 4:
        continue

    if arg['proxy']:
        continue

    # scp
    #test_command = ''.join(('scp -r -P', arg['port'], ' ', _dir_name, "/ ", arg['username'], "@", arg['host'], ":", _dir_name, "/ "))
    #print 'DOING:', test_command
    #stdin, stdout, stderr = ssh.exec_command(test_command)
    #print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())

    # run on target server
    test_command = ''.join(('cd ', _dir_name, ' && python ', _ssh_test_file_name, ' ', defaultfilename))
    print 'DOING:', test_command
    stdin, stdout, stderr = ssh.exec_command(test_command)
    print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())
