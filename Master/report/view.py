#coding:utf8
import tornado
import json

from base_def import APIBaseHandler, MainJsonEncoder
from user.view import authenticated
from .model import ReportControl

class APIReportControlHandler(APIBaseHandler):
    '''
    get:
        get report status or range

    post:
        add a new report

    del:
        del all report
    '''
    @authenticated
    def get(self):
        by = self.get_argument('by')
        if by == 'status':
            base_info = {'total_count':ReportControl.get_report_count()}
            self.write(base_info)
        elif by == 'range':
            start = int(self.get_argument("start"))
            count = int(self.get_argument("count"))
            report_list = ReportControl.get_report_by_range(start, start+count)
            self.write(json.dumps(report_list, cls=MainJsonEncoder))
        else:
            raise HTTPError(400)

    @authenticated
    def post(self):
        music_id = self.get_argument("music_id")
        report_info = self.get_argument("report_info")
        report = ReportControl.add_report(music_id, report_info)
        self.write(json.dumps(report, cls=MainJsonEncoder))

    @authenticated
    def delete(self):
        ReportControl.remove_all_report()
        self.write({})

class APIReportHandler(APIBaseHandler):
    '''
    get:
        get report details

    delete:
        delete report
    '''

    @authenticated
    def get(self, report_id):
        report = ReportControl.get_report(report_id)
        self.write(json.dumps(report, cls=MainJsonEncoder))

    @authenticated
    def delete(self, report_id):
        report = ReportControl.get_report(report_id)
        report.remove()
        self.write({})

# class ReportControlHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("music.html")
