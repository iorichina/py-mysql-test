# py-mysql-test
python scripts for testing mysql.

## connection test
test whether current system could create a connection to special database.

usage:

```python connect-test.py [connect-test.args.json file name]```

```python connect-test.py host      port user   passwd      database_name   [charset]```

```python connect-test.py 127.0.0.1 3307 fg     k014        star```

```python connect-test.py 127.0.0.1 3306 fag    'A1^>b8D'   foaore          utf8mb4```

## dependencies
<pre>
    PyMySQL==0.7.9          (from PyMySQL==0.7.9)
</pre>