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
4. requests
5. beautifulsoup4
6. APScheduler

Settings
--------

### Master

1. edit the info in `master_config.py` and then run `python master_config.py`.

2. run `python main.py` to start service.

3. run `python scheduler.py` to start background sched.
