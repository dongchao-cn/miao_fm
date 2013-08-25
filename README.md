miao_fm
=======

this is a online music server, just like douban FM

Depends
-------

### Softwares
1. Python 2.X
2. mongodb
3. nginx
4. lame

### Python Packages
1. tornado
2. mongoengine

Settings
--------

### Server

- config.py

edit the info about server and then run `python config.py` to generate `server_nginx.config` and `cdn_nginx.config`

edit `nginx.conf` and include the 2 config file above.

RunServer
---------

```
python main.py
```

