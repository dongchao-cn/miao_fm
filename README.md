miao_fm
=======

this is a online music server, just like douban FM.

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
3. mutagen

Settings
--------

### Master



- master_config.py

1. edit the info and then run `python master_config.py` to config.

2. run `python main.py 2>> master.log` to start service.

### Slave

Optional, it is using as cdn.

- slave_config.py

1. edit the info and then run `python slave_config.py` to config.

2. run `python main.py 2>> slave.log` to start service.

