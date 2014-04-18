miao_fm
=======

this is a online music server, just like douban FM.

**This project is deprecated and will NO longer be updated！**
Please see [wang_fm](https://github.com/dccrazyboy/wang_fm/) instead.

Depends
-------

### Softwares
1. Python 2.7.X
2. mongodb 2.4.8
3. lame 3.99.5+repack1-3

### Python Packages
1. tornado==3.1.1
2. mongoengine==0.8.4
3. mutagen==1.22
4. requests==2.0.1
5. beautifulsoup4==4.3.2
6. APScheduler==2.1.1
7. celery==3.1.5

Settings
--------

### Master

In `Master`, exec this:

1. run `python config.py` to generate a `master_config.py` and config the site.

2. run `python main.py` to start service.

3. run `python scheduler.py` to start background sched.

4. run `celery -A tasks worker` to start celery tasks.

Note: You may need [supervisord](http://supervisord.org/) to manage all of this.
