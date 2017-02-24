# Pyredis

**Have to close this project until I have money for private...**

A DB store Key-Value written by python like redis for fun.

# Usage

**Server**
```
$ python kv_server [-h] [-d] [--host 127.0.0.1] [--port 5678] [--authconfig auth.conf]
```

**Client**
```
usage: kv_client [-h] [-d] [--host 127.0.0.1] [--port 5678] {SET,GET,AUTH,URL,SHELL} 
```

- Subcommand:
  - `python kv_client SHELL`: Open a interact shell, can execute SET, GET, AUTH, URL, HELP command.
  - `python kv_client SET key value`: Set k-v.
  - `python kv_client GET key`: Get value by key.
  - `python kv_client AUTH username password`: Auth user for executing URL command, if match return 0 else return -1.
  - `python kv_client URL name url`: return url's status_code and len.

# Example

```
$ python kv_server.py --authconfig auth.conf
Pyredis listening in: ('127.0.0.1', 5678) ...
connected from: ('127.0.0.1', 52916) <Thread(Thread-1, started daemon 140632751793920)>
disconnect : ('127.0.0.1', 52916) <Thread(Thread-1, started daemon 140632751793920)>
...


$ python kv_client.py SHELL
Help:
    SET key value           Set value.
    GET key
    AUTH username password
    URL name url
    QUIT|quit|EXIT|exit|q       close termimal

> SET a
(1, 'Only need three arguements(SET key value).')
> SET a 123
0
> GET a
123
> URL baidu www.baidu.com
None
> AUTH czw 123456
0
> URL baidu www.baidu.com
(200, 102156)
> quit


$ python kv_client.py SET b 456
0
$ python kv_client.py GET b 
456
```

