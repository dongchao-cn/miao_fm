#coding:utf8
import tornado
import json

from util import APIBaseHandler, MainJsonEncoder
from user.model import authenticated
from .model import ReportSet

class APIReportSetHandler(APIBaseHandler):
    '''
    get:
        get report status or range

    post:
        add a new report

    del:
        del all report
    '''
    @authenticated(['uploader', 'admin'])
    def get(self):
        by = self.get_argument('by')
        if by == 'status':
            base_info = {'total_count':ReportSet.get_report_count()}
            self.write(base_info)
        elif by == 'range':
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
            report_list = ReportSet.get_report_by_range(start, start+count)
            self.write(report_list)
        else:
            raise HTTPError(400)

    def post(self):
        music_id = self.get_argument("music_id")
        report_info = self.get_argument("report_info")
        report = ReportSet.add_report(music_id, report_info)
        self.write(report)

    @authenticated(['uploader', 'admin'])
    def delete(self):
        ReportSet.remove_all_report()
        self.write(None)

class APIReportHandler(APIBaseHandler):
    '''
    get:
        get report details

    delete:
        delete report
    '''

    @authenticated(['uploader', 'admin'])
    def get(self, report_id):
        report = ReportSet.get_report(report_id)
        self.write(report)

    @authenticated(['uploader', 'admin'])
    def delete(self, report_id):
        report = ReportSet.get_report(report_id)
        report.remove()
        self.write(None)

class ReportHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("report.html")
