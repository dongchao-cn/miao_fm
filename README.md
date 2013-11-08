miao_fm
=======

this is a online music server, just like douban FM.

Depends
-------

### Softwares
1. Python 2.X
2. mongodb
3. lame

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

1. run `python config.py` to generate a `master_config.py` and config the db.

2. run `python main.py` to start service.

3. run `python scheduler.py` to start background sched.
