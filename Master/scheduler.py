#! /usr/bin/env python
#coding=utf-8
import datetime
import traceback
from apscheduler.scheduler import Scheduler
from music.get_music_tag import update_the_tag
from status.model import gen_status, gc


def update_all():
    print '[update_all] start', datetime.datetime.now()
    try:
        print '[gc] start', datetime.datetime.now()
        gc()
        print '[gc] finish', datetime.datetime.now()
    except:
        print '[gc] error!', datetime.datetime.now()
        traceback.print_exc()

    try:
        print '[update_the_tag] start', datetime.datetime.now()
        update_the_tag()
        print '[update_the_tag] finish', datetime.datetime.now()
    except:
        print '[update_the_tag] error!', datetime.datetime.now()
        traceback.print_exc()

    try:
        print '[gen_status] start', datetime.datetime.now()
        gen_status()
        print '[gen_status] finish', datetime.datetime.now()
    except:
        print '[gen_status] error!', datetime.datetime.now()
        traceback.print_exc()

    print '[update_all] finish', datetime.datetime.now()

if __name__ == '__main__':
    sched = Scheduler(standalone=True)
    sched.add_cron_job(update_all, hour=2)
    # sched.add_interval_job(update_all, seconds=5)

    sched.start()
