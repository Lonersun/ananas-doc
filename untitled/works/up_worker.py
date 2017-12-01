from lcyframe.libs.mq_route import worker
from lcyframe.base import BaseObject
from tornado.gen import Return, coroutine

@worker("up")
class func(BaseObject):
    @classmethod
    @coroutine
    def do(cls, msg):
        print msg
        raise Return(True)
