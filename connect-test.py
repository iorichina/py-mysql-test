#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import time
import os
import json
from sys import argv
import sys

print "system timestamp:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def readjsonfile( filename ):
    if not os.path.exists(filename):
        print "args file [", filename,"] not exists"
        sys.exit()
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

    return args

args = [{}]
_port=3306
_charset="utf8"

if len(argv) == 1:
    args = readjsonfile('connect-test.args.json')
elif len(argv) == 2:
    args = readjsonfile(argv[1])
elif len(argv) < 6 or len(argv) > 7:
    print "usage: "
    print "]$ python connect-test.py [connect-test.args.json]"
    print "]$ python connect-test.py host      port user   passwd      database_name   [charset]"
    print "]$ python connect-test.py 127.0.0.1 3307 fg     k014        star"
    print "]$ python connect-test.py 127.0.0.1 3306 fag    'A1^>b8D'   foaore          utf8mb4"
    sys.exit()

if len(argv) > 5:
    args[0]['host']=argv[1]
    args[0]['port']=int(argv[2])
    args[0]['user']=argv[3]
    args[0]['passwd']=argv[4]
    args[0]['db']=argv[5]
    args[0]['charset']=_charset

    if len(argv) > 6:
        args[0]['charset']=argv[6]

print "args:", args

# loop each database
for dbarg in args:
    print ""
    # database params
    host = dbarg['host']
    port = _port
    user = dbarg['user']
    passwd = dbarg['passwd']
    db = dbarg['db']
    charset = _charset

    if dbarg.has_key('port'):
        port = dbarg['port']
    if dbarg.has_key('charset'):
        charset = dbarg['charset']

    # thisdbstr = "".join(tuple(dbarg))
    thisdbstr = "[{0}:{1}]".format(host, port)
    print "testing:", thisdbstr

    result=[]
    try:
        conn=pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        try:
            cur=conn.cursor()
            cur.execute("SELECT UNIX_TIMESTAMP(), NOW()")
            cur.close()
            result=cur.fetchall()
        except Exception, e:
            print thisdbstr, "test fail: ", e.args
            continue
        finally:
            conn.close()
    except pymysql.err.OperationalError, oe:
        print thisdbstr, "test fail: ", oe.args
        continue
    except pymysql.err.InternalError, oe:
        print thisdbstr, "test fail: ", oe.args
        continue
    except UnicodeDecodeError, e:
        print thisdbstr, "test fail: ", e, (e.args)
        continue

    print thisdbstr, "database timestamp:", result[0][1]
    #
    #print "test ok" if int(time.time()) - result[0][0] < 60 else "test fail"
    #python 2.4
    if int(time.time()) - result[0][0] < 600:
        print thisdbstr, "test ok"
    else:
        print thisdbstr, "test fail"

