#! /usr/bin/env python
#coding=utf-8
from apscheduler.scheduler import Scheduler
from music.get_music_tag import update_the_tag

sched = Scheduler(standalone=True)
sched.add_cron_job(update_the_tag, hour=2)
# sched.add_interval_job(update_the_tag, seconds=5)

sched.start()
