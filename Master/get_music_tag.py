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
from master_config import MONGODB_URL, MONGODB_PORT, update_tag_time

schedule = sched.scheduler(time.time, time.sleep) 

def getmusicnum(musicname, singername):
    print musicname,singername
    url = 'http://www.xiami.com/search?key='+musicname
    header = {'Referer':'http://www.xiami.com','User-Agent':'Mozilla/5.0'}
    try:
        r = requests.get(url,headers = header)
    except:
        print 'except'
        return None
    soup = BeautifulSoup(r.text)
    body = soup.find('body')
    # print body
    result_main = body.findAll(class_ = 'result_main')
    # print result_main
    retr = result_main[0].findAll('tr')
    song_num = None
    for each in retr[1:]:
        # tdartist = each.findAll(class_='song_artist')[0].a['title'].encode('utf-8')
        tdartist = each.findAll(class_='song_artist')[0].a['title']
        if ''.join(tdartist.split()).upper() == ''.join(singername.split()).upper():
            tdname = each.findAll(class_='song_name')[0].a#.findNextSibling('a')['href']
            while tdname['href'] == "javascript:;":
                tdname = tdname.findNextSibling('a')
            # print tdname['href']
            song_num = tdname['href'][len(u'/song/'):]
            break
    return song_num

def getmusictags(song_num):
    tagurl = 'http://www.xiami.com/song/moretags/id/'+str(song_num)
    header = {'Referer':'http://www.xiami.com','User-Agent':'Mozilla/5.0'}
    print tagurl
    try:
        r = requests.get(tagurl,headers = header)
    except:
        return None
    soup = BeautifulSoup(r.text)
    # print soup
    tag_cloud = soup.findAll(class_ = 'tag_cloud')
    tag_dic = {}
    span = tag_cloud[0].findAll('span')
    for i in span:
        tag_dic[i.a.text.encode('utf-8')] = int(i.a['class'][0].split('_')[1])
    tag_dic['update_datetime'] = datetime.datetime.now()
    return tag_dic

def getmusicimg(song_num):
    imgurl = 'http://www.xiami.com/song/'+str(song_num)
    header = {'Referer':'http://www.xiami.com','User-Agent':'Mozilla/5.0'}
    try:
        r = requests.get(imgurl,headers = header)
    except:
        return None
    soup = BeautifulSoup(r.text)
    imgtag = soup.findAll(class_ = 'cdCDcover185')
    return imgtag[0]['src']



def perform_command( inc): 
    # 安排inc秒后再次运行自己，即周期运行 
    schedule.enter(inc, 0, perform_command, ( inc,)) 
    # os.system(cmd)
    print 'start at %s' % (datetime.datetime.now())
    Musics = Music.objects()
    for music in Musics:
        music_name = music['music_name']
        music_artist = music['music_artist']
        music_num = getmusicnum(music_name,music_artist)
        if not music_num:
            return
        music_tags = getmusictags(music_num)
        music_img = getmusicimg(music_num)
        print music_tags
        print music_img
        music['music_tag'] = music_tags
        music['music_img'] = music_img
        music.save()
        # print music['music_name']
        # print music['music_artist']
        # print music['music_tag']
        # print music['music_img']
    print 'end at %s' % (datetime.datetime.now())
       
def timming_exe(inc = 60): 
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动 
    schedule.enter(inc, 0, perform_command, ( inc,)) 
    # 持续运行，直到计划时间队列变成空为止 
    schedule.run() 
       
if __name__ == '__main__':
    connect('miao_fm', host=MONGODB_URL ,port=MONGODB_PORT)
    # print("show time after 10 seconds:") 
    timming_exe(update_tag_time)
