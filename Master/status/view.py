#coding:utf8
from tornado.httpclient import HTTPError

from util import APIBaseHandler
from .model import Status


class APIStatusHandler(APIBaseHandler):
    '''
    get:
        get status
    '''
    def get(self):
        by = self.get_argument('by')
        if by == 'last':
            status = Status.objects()[0]
            status.get_brief_status()
            self.write(status)
        else:
            raise HTTPError(400)
