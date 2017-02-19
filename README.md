# py-mysql-test
python scripts for testing mysql.

## installation
```python -m pip install -r requirements.txt --prefix . -I```

and/or copy the lib `pymysql` into this project root directory.

or just use branch full_version_with_libs.

[scp.py](https://github.com/jbardin/scp.py) is already included.

## connection test
test whether current system could create a connection to special database.

usage:

```python connect-test.py host      port user   passwd      database_name   [charset]```

```python connect-test.py 127.0.0.1 3307 fg     k014        star```

```python connect-test.py 127.0.0.1 3306 fag    'A1^>b8D'   foaore          utf8mb4```

## ssh connection test
test whether the ssh logined systems could create a connection.

usage:

```python ssh-connect-test.py [filename(default 'ssh-connect-test.args.json')]```

```python ssh-connect-test.py test-args.json```

## dependencies
<pre>
    PyMySQL==0.7.9          (from PyMySQL==0.7.9)
    paramiko==2.0.2         (from paramiko==2.0.2)
    pycrypto==2.6.1         (from pycrypto==2.6.1)
    pyasn1>=0.1.7           (from paramiko==2.0.2->paramiko==2.0.2)
    cryptography>=1.1       (from paramiko==2.0.2->paramiko==2.0.2)
    setuptools>=11.3        (from cryptography>=1.1->paramiko==2.0.2->paramiko==2.0.2)
    enum34                  (from cryptography>=1.1->paramiko==2.0.2->paramiko==2.0.2)
    ipaddress               (from cryptography>=1.1->paramiko==2.0.2->paramiko==2.0.2)
    six>=1.4.1              (from cryptography>=1.1->paramiko==2.0.2->paramiko==2.0.2)
    idna>=2.0               (from cryptography>=1.1->paramiko==2.0.2->paramiko==2.0.2)
    cffi>=1.4.1             (from cryptography>=1.1->paramiko==2.0.2->paramiko==2.0.2)
    pycparser               (from cffi>=1.4.1->cryptography>=1.1->paramiko==2.0.2->paramiko==2.0.2)
</pre>