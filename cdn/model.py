#!/usr/bin/env python
#coding:utf8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
from mongoengine import *

connect('miao_fm')

class Cdn(Document):
    '''
    store cdn info
    '''
    name = StringField(max_length=100,primary_key=True)
    url_path = StringField(max_length=50)

    def __str__(self):
        return ('%s' % (self.name)).encode('utf-8')

    @property
    def url(self):
        '''
        get url
        '''
        return self.url_path

class CdnControl(object):
    '''
    CDN control functions
    '''

    def __init__(self):
        raise Exception,'CdnControl can\'t be __init__'

    @classmethod
    def add_cdn(cls, name, url_path):
        '''
        add new cdn
        if cdn_name exist, rewrite it
        '''
        Cdn(name, url_path).save()

    @classmethod
    def del_cdn(cls, name):
        '''
        del cdn from db
        '''
        Cdn.objects(name=name).first().delete()

    @classmethod
    def get_all_cdn(cls):
        '''
        get all cdn from db
        '''
        return Cdn.objects()

if __name__ == '__main__':
    cnd1 = Cdn("xidian1",'cdn1.xidian.com')
    cnd1.save()
    print cnd1.url
    cnd2 = Cdn("xidian2",'cdn2.xidian.com').save()
    cnd2.save()

    CdnControl.add_cdn("xidian1",'cdn1.xidian.com')
    CdnControl.add_cdn("xidian2",'cdn2.xidian.com')
    print CdnControl.get_all_cdn()
    CdnControl.del_cdn("xidian2")
    print CdnControl.get_all_cdn()