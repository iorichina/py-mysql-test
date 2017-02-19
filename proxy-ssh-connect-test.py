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
    print "]$ python proxy-ssh-connect-test.py host      port   user    passwd  [ssh-args-file(default '",defaultfilename,"')]"
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

# upload file name
_pip_file_name="get-pip.py"
if "2.6" in _stdout or "2.6" in _stderr:
    _pip_file_name="get-pip-2.6.py"

_dir_name = "py-mysql-test"

_do_upload = True

if _do_upload:
    print 'doing upload'
    
    _file_names = {_pip_file_name:False, 'scp.py':False, 'proxy-pip-install.py':False, "connect-test.py":False, "ssh-connect-test.py":False, "requirements.txt":False}
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

# print 'doing run ', _pip_file_name
# test_command = ''.join(('cd ', _dir_name, ' && python ', _pip_file_name, ' --prefix . -I'))
# stdin, stdout, stderr = ssh.exec_command(test_command)
# _stdout = ''.join(stdout.readlines())
# _stderr = ''.join(stderr.readlines())
# print proxystr, _stdout, _stderr
# if 'Could not' in _stdout or 'Could not' in _stderr:
#     sys.exit()

print 'doing ls',_dir_name
test_command = ''.join(('ls ', _dir_name))
stdin, stdout, stderr = ssh.exec_command(test_command)
print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())

print 'doing pip install'
test_command = ''.join(('cd ', _dir_name, ' && python proxy-pip-install.py'))
stdin, stdout, stderr = ssh.exec_command(test_command)
print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())

print 'doing ssh connect test'
test_command = ''.join(('cd ', _dir_name, ' && python ssh-connect-test.py ', defaultfilename))
stdin, stdout, stderr = ssh.exec_command(test_command)
print proxystr, ''.join(stdout.readlines()), ''.join(stderr.readlines())