#! /usr/bin/env python
#coding=utf-8
import time, os, sched 
from music.model import Music
import socket
import requests
import re
import datetime
from bs4 import BeautifulSoup
from mongoengine import *
from master_config import MONGODB_URL, MONGODB_PORT, update_tag_time, update_tag_thresh_day


if __name__ == '__main__':
    connect('miao_fm', host=MONGODB_URL ,port=MONGODB_PORT)
    Musics = Music.objects()
    for music in Musics:
    	# if music.has_key('music_img') == False:
    	# 	print music['music_name']
    	print music['music_name']
    	print music['music_img']