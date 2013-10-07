#!/usr/bin/env python
#coding:utf8
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../')
import json
import datetime

from mongoengine import *
from bson.objectid import ObjectId

from master_config import MASTER_CDN, MASTER_MONGODB_PORT

from music.model import Music, MusicSet

# connect('miao_fm', host='127.0.0.1' ,port=MASTER_MONGODB_PORT)

class Report(Document):
    '''
    store report info
    all item and functions start with *report_* will be auto serialized
    '''
    report_music = ReferenceField(Music, reverse_delete_rule=CASCADE)

    report_info = StringField(max_length=200, default='')
    report_date = DateTimeField()

    @property
    def report_id(self):
        return self.pk

    meta = {
        'ordering': ['-report_date']
    }

    def __str__(self):
        return ('report_music = %s report_info = %s\n' % \
            (self.report_music.music_id, self.report_info)).encode('utf-8')

    def remove(self):
        self.delete()

class ReportSet(object):
    '''
    Report control functions
    '''

    def __init__(self):
        raise Exception,'ReportSet can\'t be __init__'

    @classmethod
    def add_report(cls, report_music_id, report_info):
        music = MusicSet.get_music(report_music_id)
        if music:
            report = Report(report_music=music, report_info=report_info,
                report_date=datetime.datetime.now()).save()
            return report
        else:
            return

    @classmethod
    def get_report(cls, report_id):
        try:
            return Report.objects(pk=report_id).first()
        except ValidationError:
            return None

    @classmethod
    def remove_all_report(cls):
        for report in Report.objects():
            report.remove()

    @classmethod
    def get_report_by_range(cls, start, end):
        return [each for each in Report.objects[start : end]]

    @classmethod
    def get_report_count(cls):
        return Report.objects().count()

if __name__ == '__main__':
    connect('miao_fm', host='127.0.0.1' ,port=MASTER_MONGODB_PORT)
    # report = ReportSet.add_report('524ffdf056a9e50cbb93a443','dasd')
    # print report
    report = ReportSet.get_report_by_range(0,10)[0]
    print json.dumps(report, cls=ReportJsonEncoder)