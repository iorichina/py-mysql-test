import pymysql
import time
import sys
from sys import argv
import json
from scp import SCPClient
import paramiko

print "current system timestamp:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

filename = "ssh-connect-test.args.json"
if len(argv) > 2:
    print "usage: "
    print "]$ python ssh-connect-test.py [filename(default 'args.ssh-connect-test.json')]"
    print "]$ python ssh-connect-test.py test-args.json"
    sys.exit()

if len(argv) > 1:
    filename = argv[1]

# checkout arguments file
args = []
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

_host=""#not null
_port=3306
_user=""#not null
_passwd=""#not null
_db=""#not null
_charset="utf8"

# upload file name
_dir_name = "py-mysql-test"
_test_file_name = "connect-test.py"
_pymysql_dir_name = "pymysql"

# loop each ssh server
for arg in args:
    if len(arg) < 4:
        pass

    thissshstr = "".join(("[", arg['host'], ":", str(arg['port']), "]"))
    # ssh logn 
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(arg['host'],arg['port'],arg['username'],arg['password'],timeout=5)

    # TODO:test python version
    stdin, stdout, stderr = ssh.exec_command('python -V')
    print thissshstr, ''.join(stdout.readlines()), ''.join(stderr.readlines())

    # SCPCLient takes a paramiko transport as its only argument
    scp = SCPClient(ssh.get_transport())

    # upload files
    try:
        ssh.exec_command('mkdir -p ' + _dir_name)
        scp.put(_test_file_name, _dir_name)
        scp.put(_pymysql_dir_name, _dir_name, True)
    finally:
        scp.close()
        pass

    # loop each database
    for dbarg in arg['db']:
        # database params
        host = dbarg['host']
        port = _port
        if dbarg.has_key('port'):
            port = dbarg['port']
        user = dbarg['user']
        passwd = dbarg['passwd']
        db = dbarg['db']
        charset = _charset
        if dbarg.has_key('charset'):
            charset = dbarg['charset']

        db_test_params = ' '.join((host, str(port), user, passwd, db, charset))
        db_test_command = ''.join(('cd ', _dir_name, ' && python ', _test_file_name, ' ', db_test_params))
        stdin, stdout, stderr = ssh.exec_command(db_test_command)

        print thissshstr, ''.join(stdout.readlines()), ''.join(stderr.readlines())
