# py-mysql-test
python scripts for testing mysql

## installation
```pip install -r requirements.txt```

## connection test
test whether current system could create a connection to special database.

usage:

```python connect-test.py host      port user   passwd      database_name   [charset]```

```python connect-test.py 127.0.0.1 3307 fg     k014        star```

```python connect-test.py 127.0.0.1 3306 fag    'A1^>b8D'   foaore          utf8mb4```

## ssh connection test
test whether the ssh logined systems could create a connection

usage:

```python ssh-connect-test.py [filename(default 'ssh-connect-test.args.json')]```

```python ssh-connect-test.py test-args.json```
