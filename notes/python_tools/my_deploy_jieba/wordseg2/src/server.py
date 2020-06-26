# encoding:utf-8
import json
import logging.config
import math
import os
import time
from multiprocessing import Manager, Process, current_process, cpu_count

import jieba
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# 服务进程数
PROCESS_NUM = 1
# jieba分词子进程数
CONSUMER_NUM = cpu_count() - 1 if cpu_count() - 1 > 0 else 2
# 文本行数超过指定数值时使用多进程来分词
BATCH_START_LINES = 2000

LOG_CONF = os.path.abspath(
    os.path.join(os.getcwd(), '../conf/log.conf')
)
logging.config.fileConfig(LOG_CONF)
ilog_root = logging.getLogger('root')
ilog_info = logging.getLogger('info')


def _run_producer():
    # 生产者子进程
    producer_p = Process(target=_producer, args=(text_q, broker))
    producer_p.start()


def _run_consumer(processes=CONSUMER_NUM):
    # 消费者子进程
    for _ in range(processes):
        process = Process(target=_consumer, args=(broker, backend))
        process.start()


def _producer(text_q, broker):
    # print 'producer %s standby' % current_process().name
    ilog_info.info('producer %s standby' % current_process().name)

    while True:
        text_li = text_q.get()
        # print 'producer %s receive a text_li' % current_process().name
        ilog_info.info('producer %s receive a text_li' % current_process().name)

        _len = len(text_li)
        # print 'total lines: %s' % _len
        ilog_info.info('total lines: %s' % _len)
        size = math.ceil(_len / CONSUMER_NUM)
        for i in range(CONSUMER_NUM):
            start = int(i * size)
            stop = int((i + 1) * size)
            text = '\n'.join(text_li[start:stop])
            broker.put(dict(text=text, index=i))
            # print 'producer %s put a item to broker' % current_process().name


def _consumer(broker, backend):
    # print 'consumer %s standby' % current_process().name
    ilog_info.info('consumer %s standby' % current_process().name)
    # jieba init, load model from cache
    jieba.cut('init')

    while True:
        ret = broker.get()
        # print 'consumer %s get a item from broker' % current_process().name
        seg_list = jieba.lcut(ret['text'], HMM=False)
        backend.put(dict(
            seg_list=seg_list,
            index=ret['index'],
        ))
        # print 'consumer %s put a result to backend' % current_process().name


def _parse_ret():
    result = list()
    count = 0
    while count < CONSUMER_NUM:
        ret = backend.get()
        # print ret['index'], CONSUMER_NUM
        ilog_info.info('index: %s, process num: %s' % (ret['index'], CONSUMER_NUM))
        result.append(ret)
        count += 1
    result = sorted(result, key=lambda x: x['index'])
    seg_list = list()
    for item in result:
        seg_list.extend(item['seg_list'])
    return seg_list


class WordsegHandler(tornado.web.RequestHandler):
    def post(self):
        # print 'RECEIVE: %s' % self.request.body
        ilog_info.info('RECEIVE: %s' % self.request.body[:100])
        dic = json.loads(self.request.body or '{}')
        text = dic.get('text', '')
        if not text:
            ilog_root.error('Argument `text` is required in request json data')
            return self.write('text is required')

        start = time.time()
        text_li = text.split('\n')
        # 不用多进程的情况
        if len(text_li) < BATCH_START_LINES:
            seg_list = jieba.lcut(text, HMM=False)
            # print 'seg count: %s' % len(seg_list)
            ilog_info.info('seg count: %s' % len(seg_list))
            cost = time.time() - start
            speed = len(seg_list) / cost * 1000
            result = dict(results=seg_list, cost=cost, speed=speed)
            return self.write(json.dumps(result, ensure_ascii=False))

        # 使用多进程分词
        text_q.put(text_li)
        seg_list = _parse_ret()
        # print 'seg count: %s' % len(seg_list)
        ilog_info.info('seg count: %s' % len(seg_list))
        cost = time.time() - start
        speed = len(seg_list) / cost * 1000
        result = dict(results=seg_list, cost=cost, speed=speed)
        self.write(json.dumps(result, ensure_ascii=False))


def main():
    app = tornado.web.Application(handlers=[(r"/wordseg/", WordsegHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(8001)
    http_server.start(PROCESS_NUM)
    print 'init'
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    manager = Manager()
    text_q = manager.Queue()
    broker = manager.Queue()
    backend = manager.Queue()
    _run_producer()
    _run_consumer()
    main()
