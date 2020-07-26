# coding=utf-8
import json
import time

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado import gen


class BlockingHandler(tornado.web.RequestHandler):
    def get(self):
        print 'deal with one request', time.time()
        time.sleep(5)
        self.write('blocking')


class NonBlockingHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        ret = yield self.doing()
        print ret
        self.write(json.dumps({'message': 'non-blocking'}, ensure_ascii=False))

    @gen.coroutine
    def doing(self):
        """
        穿上@gen.coroutine 装饰器之后，最终结果会返回一个可以被 yield 的生成器 Future 对象
        与众不同的是这个函数的返回值需要以 raise gen.Return() 这种形式返回。
        :return: Future object
        """
        print 'deal with one request', time.time()
        # time.sleep(10)     # time.sleep() 是 blocking 的，不支持异步操作
        yield gen.sleep(5)  # 可以点进去看下这个方法的介绍
        raise gen.Return('Non-Blocking')


def main():
    # import subprocess
    # subprocess.Popen('python tornado_test_request.py', shell=True)

    app = tornado.web.Application(handlers=[
        (r"/blocking/", BlockingHandler),
        (r"/non-blocking/", NonBlockingHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(8005)
    http_server.start(1)
    print 'server init'
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
