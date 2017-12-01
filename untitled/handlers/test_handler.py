# coding=utf-8
from lcyframe.base import BaseHandler
from lcyframe.libs.route import route

@route("/test")
class TestHandler(BaseHandler):

    def get(self):
        p = self.params
        # print self.application.db.users.find_one()
        # self.application.redis.set("a", 12)
        # self.application.ssdb.set("a", 12)
        self.application.mq.put({"action": "up", "a": 1})
        self.write_success(p)

    def post(self):
        p = self.params
        self.write_success(p)

