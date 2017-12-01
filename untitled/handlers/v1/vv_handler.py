# coding=utf-8
from lcyframe.base import BaseHandler
from lcyframe.libs.route import route

@route("/vv")
class VVHandler(BaseHandler):

    def get(self):
        p = self.params
        self.write_success(p)

    def post(self):
        p = self.params
        self.write_success(p)

