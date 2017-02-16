import pymysql
import time
import sys
from sys import argv

print "system timestamp:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

if len(argv) < 6 or len(argv) > 7:
    print "usage: "
    print "]$ python connect-test.py host      port user   passwd      database_name   [charset]"
    print "]$ python connect-test.py 127.0.0.1 3307 fg     k014        star"
    print "]$ python connect-test.py 127.0.0.1 3306 fag    'A1^>b8D'   foaore          utf8mb4"
    sys.exit()

host=""
port=3306
user=""
passwd=""
db=""
charset="utf8"

if len(argv) > 5:
    host=argv[1]
    port=int(argv[2])
    user=argv[3]
    passwd=argv[4]
    db=argv[5]

    if len(argv) > 6:
        charset=argv[6]

thisdbstr = "".join(("[", host, ":", str(port), "]"))

result=[]
try:
    conn=pymysql.connect(host=host, port=port, user=user, passwd=passwd,db=db, charset=charset)
    cur=conn.cursor()
    cur.execute("SELECT UNIX_TIMESTAMP(), NOW()")
    cur.close()
    conn.close()

    result=cur.fetchall()
except pymysql.err.OperationalError, oe:
    print thisdbstr, "test fail: ", oe.args
    sys.exit()

print thisdbstr, "database timestamp:", result[0][1]
#
#print "test ok" if int(time.time()) - result[0][0] < 60 else "test fail"
#python 2.4
if int(time.time()) - result[0][0] < 60:
    print thisdbstr, "test ok"
else:
    print thisdbstr, "test fail"