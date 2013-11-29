#! /usr/bin/env python
#coding=utf-8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import random
import requests
import datetime
import traceback
from bs4 import BeautifulSoup
from jft import *
from mongoengine import *

from music.model import Music
from master_config import MONGODB_URL, MONGODB_PORT, update_tag_thresh_day, update_tag_thresh_random


def getmusicnum(musicname, singername):
    print musicname.encode('utf8'), singername.encode('utf8')
    if musicname == '':
        print 'no name'
        return None
    url = 'http://www.xiami.com/search?key='+musicname
    header = {'Referer': 'http://www.xiami.com', 'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=header)
    except:
        print 'except'
        return None
    soup = BeautifulSoup(r.text)
    body = soup.find('body')
    # print body
    result_main = body.findAll(class_='result_main')
    # print result_main
    retr = result_main[0].findAll('tr')
    song_num = None
    for each in retr[1:]:
        # tdartist = each.findAll(class_='song_artist')[0].a['title'].encode('utf-8')
        tdartist = each.findAll(class_='song_artist')[0].a['title']
        if ''.join(tdartist.split()).upper() == ''.join(singername.split()).upper():
            tdname = each.findAll(class_='song_name')[0].a  # .findNextSibling('a')['href']
            while tdname['href'] == "javascript:;":
                tdname = tdname.findNextSibling('a')
            # print tdname['href']
            # song_num = tdname['href'][len(u'/song/'):]
            song_num = each.findAll(class_ = 'chkbox')[0].input['value']
            return song_num
    for each in retr[1:]:
        tdname = each.findAll(class_='song_name')[0].a
        if tdname['href'] == "javascript:;":
            while tdname['href'] == "javascript:;":
                tdname = tdname.findNextSibling('a')
        # tdartist = each.findAll(class_='song_artist')[0].a['title'].encode('utf-8')
        if ''.join(tdname['title'].split()).upper() == ''.join(musicname.split()).upper():
            # tdname = each.findAll(class_='song_name')[0].a#.findNextSibling('a')['href']
            # while tdname['href'] == "javascript:;":
            #     tdname = tdname.findNextSibling('a')
            # print tdname['href']
            # song_num = tdname['href'][len(u'/song/'):]
            song_num = each.findAll(class_ = 'chkbox')[0].input['value']
            return song_num
    return song_num


def getmusictags(song_num):
    tagurl = 'http://www.xiami.com/song/moretags/id/'+str(song_num)
    header = {'Referer': 'http://www.xiami.com', 'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(tagurl, headers=header)
    except:
        return None
    soup = BeautifulSoup(r.text)
    # print soup
    tag_cloud = soup.findAll(class_='tag_cloud')
    tag_dic = {}
    span = tag_cloud[0].findAll('span')
    for i in span:
        tag_dic[i.a.text.encode('utf-8')] = int(i.a['class'][0].split('_')[1])
    tag_dic['update_datetime'] = datetime.datetime.now()
    return tag_dic


def getmusicimg(song_num):
    imgurl = 'http://www.xiami.com/song/'+str(song_num)
    print imgurl
    header = {'Referer': 'http://www.xiami.com', 'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(imgurl, headers=header)
    except:
        return None
    soup = BeautifulSoup(r.text)
    imgtag = soup.findAll(class_='cdCDcover185')
    return imgtag[0]['src']


def update_the_tag():
    # print 'update_the_tag', datetime.datetime.now()
    connect('miao_fm', host=MONGODB_URL, port=MONGODB_PORT)
    Musics = Music.objects()
    for music in Musics:
        try:
            nowday = datetime.datetime.now()
            if 'update_datetime' in music['music_tag'] and \
                (nowday - music['music_tag']['update_datetime']).days < \
                update_tag_thresh_day + random.randint(-update_tag_thresh_random, update_tag_thresh_random):
                # print 'continue'
                continue
            music_name = music['music_name']
            music_artist = music['music_artist']
            new_music_name = f2j('utf-8','utf-8',music_name.encode('utf-8')).decode('utf-8')
            new_music_artist = f2j('utf-8','utf-8',music_artist.encode('utf-8')).decode('utf-8')
            music_num = getmusicnum(new_music_name,new_music_artist)
            if not music_num:
                music_num = getmusicnum(music_name, music_artist)
            music['music_tag']['update_datetime'] = nowday
            if not music_num:
                music.save()
                continue
            music_tags = getmusictags(music_num)
            music_img = getmusicimg(music_num)
            print music_tags
            print music_img
            music['music_tag'] = music_tags
            music['music_img'] = music_img
            try:
                music.save()
            except:
                try:
                    music['music_tag'] = {}
                    music.save()
                except:
                    print 'on save error!'
                pass
        except:
            traceback.print_exc()
        # print music['music_name']
        # print music['music_artist']
        # print music['music_tag']
        # print music['music_img']

if __name__ == '__main__':
    print 'test main'
    update_the_tag()
