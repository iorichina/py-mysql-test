import pymysql
import time
import sys
from sys import argv
import SSHLibrary
import json

print "system   timestamp:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

filename = "ssh-connect-test.args.json"
if len(argv) > 2:
    print "usage: "
    print "]$ python ssh-connect-test.py [filename(default 'ssh-connect-test.args.json')]"
    print "]$ python ssh-connect-test.py test-args.json"
    sys.exit()

if len(argv) > 1:
    filename = argv[1]

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

# loop each ssh server
for arg in args:
    if len(arg) < 4:
        pass

    thissshstr = "".join(("[", arg['host'], ":", str(arg['port']), "]"))
    # ssh logn 
    rlogin = SSHLibrary.SSHLibrary()
    rlogin.open_connection(host=arg['host'], port=arg['port'])
    try:
        rlogin.login(username=arg['username'], password=arg['password'])
    except RuntimeError, re:
        print thissshstr, "login fail: ", re.args
        continue

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

        thisdbstr = "".join((thissshstr, "[", host, ":", str(port), "]"))

        # try connect and select
        result=[]
        try:
            conn=pymysql.connect(host=host, port=port, user=user, passwd=passwd,db=db, charset=charset)
            cur=conn.cursor()
            cur.execute("SELECT NOW(), UNIX_TIMESTAMP()")
            cur.close()
            conn.close()

            result=cur.fetchall()
        except pymysql.err.OperationalError, oe:
            print thisdbstr, "test fail: ", oe.args
            continue

        print thisdbstr, "database timestamp:", result[0][0]
        #
        #print "test ok" if int(time.time()) - result[0][0] < 60 else "test fail"
        #python 2.4
        if int(time.time()) - result[0][1] < 60:
            print thisdbstr, "test ok"
        else:
            thisdbstr, "test fail"