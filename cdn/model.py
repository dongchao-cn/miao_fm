#!/usr/bin/env python
#coding:utf8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import random
from mongoengine import *

from master_config import MASTER_CDN, MASTER_MONGODB_PORT

connect('miao_fm', host=MASTER_CDN ,port=MASTER_MONGODB_PORT)

class Cdn(Document):
    '''
    store cdn info
    '''
    name = StringField(max_length=100,unique=True)
    url_path = StringField(max_length=50)

    def __str__(self):
        return ('%s' % (self.name)).encode('utf-8')

    @property
    def url(self):
        '''
        get url
        '''
        return self.url_path

    def update_info(self, url_path):
        '''
        update cdn info
        '''
        self.url_path = url_path
        self.save()

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
    def get_cdn(cls, name):
        '''
        del cdn from db
        '''
        return Cdn.objects(name=name).first()

    @classmethod
    def get_all_cdn(cls):
        '''
        get all cdn from db
        '''
        return Cdn.objects()

    @classmethod
    def get_free_cdn(cls):
        '''
        get all cdn from db
        '''
        assert Cdn.objects().count() != 0
        return _get_random_cdn()

def _get_random_cdn():
    '''
    get random cdn
    '''
    num = random.randint(0,Cdn.objects().count()-1)
    return Cdn.objects[num]

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