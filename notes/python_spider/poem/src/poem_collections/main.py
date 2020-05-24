import json
import math
import re
import threading
import time
from pathlib import Path
from queue import Queue

import requests
from lxml import etree

from src.poem_collections.config import DBConfig
from src.poem_collections.db import DBClient

DOMAIN = "http://yw.eywedu.com"
CATEGORY_URL_FORMAT = DOMAIN + '/gushici/ShowClass.asp?ClassID={}&page={}'
ID_START = 44
ID_END = 68
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/66.0.3359.139 Safari/537.36"
}


class Poem:

    def __init__(self,):
        self._url_queue = Queue()
        self._html_queue = Queue()
        self._content_queue = Queue()

    def get_urls(self):
        path = Path('tmp.json')
        if path.exists():
            print('从 json 中读取urls.')
            return json.load(path.open('r'))

        urls = list()
        # for _id in range(ID_START, ID_END + 1):
        for _id in [44]:
            cate_url = CATEGORY_URL_FORMAT.format(_id, 1)
            resp = self.send_request(cate_url)
            element = etree.HTML(resp.content.decode('gbk'))
            # 获取Element对象列表 / 对象属性值
            elements = element.xpath("//td[@class='main_tdbg_575']/table[2]//table//a")
            urls.extend(self._parse_elements(elements))

            total = int(element.xpath("//div[@class='show_page']//b")[0].text)
            per_page = int(element.xpath("//div[@class='show_page']//b")[1].text)
            pages = math.ceil(total / per_page)
            for next_page in range(2, pages):
                cate_url = CATEGORY_URL_FORMAT.format(_id, next_page)
                resp = self.send_request(cate_url)
                element = etree.HTML(resp.content.decode('gbk'))
                # 获取Element对象列表 / 对象属性值
                elements = element.xpath("//td[@class='main_tdbg_575']/table[2]//table//a")
                urls.extend(self._parse_elements(elements))

        print('urls 收集完成.')
        json.dump(urls, path.open('w'))
        return urls

    def run(self, req_threads=3):
        threads = list()
        # 一个线程去准备 url 列表
        th_url = threading.Thread(target=self._put_urls, args=(self.get_urls(), ))
        threads.append(th_url)
        # 多个线程去发送请求
        for _ in range(0, req_threads):
            th_req = threading.Thread(target=self._request)
            threads.append(th_req)
        th_content = threading.Thread(target=self._parse_html)
        th_save = threading.Thread(target=self._save)
        threads.append(th_content)
        threads.append(th_save)

        # 启动所有子线程
        for th in threads:
            # 设置为守护线程: 等待主线程结束后再结束
            th.setDaemon(True)
            th.start()

        # 让主线程阻塞，等待队列计数为0
        for q in [self._url_queue, self._html_queue, self._content_queue]:
            # Blocks until all items in the Queue have been gotten and processed
            q.join()

    def _put_urls(self, urls):
        for url in urls:
            self._url_queue.put(url)

    def _request(self):
        # 让子线程循环去 url 队列中取 url, 直到主线程结束后子线程就结束
        while True:
            url = self._url_queue.get()
            resp = self.send_request(url)
            if resp.status_code == 200:
                self._html_queue.put(resp.content.decode('gbk', errors='ignore'))
                # q.task_done 配合 q.join 使用,
                # q.task_done 将队列计数减1, q.join 阻塞主线程直到队列计数为0
                self._url_queue.task_done()
            else:
                self._url_queue.put(url)

    @staticmethod
    def send_request(url):
        time.sleep(1)
        return requests.get(url, headers=HEADERS)

    @staticmethod
    def _parse_elements(elements):
        results = list()
        for i in range(0, len(elements), 2):
            # 偶数位是 大类, 如`[五言绝句]`
            # 奇数位是 标题, 包含作者、诗标题等
            try:
                ele_title = elements[i+1]
            except IndexError:
                ele_title = elements[i]
            url = DOMAIN + ele_title.attrib.get("href")
            print(url)
            results.append(url)
        return results

    def _parse_html(self):
        title_pattern = re.compile("(.*?)《(.*?)》.*?")
        while True:
            html_str = self._html_queue.get()
            # 实例化Element对象
            element = etree.HTML(html_str)
            # title举例: 白居易《暮江吟》原文译文
            text = element.xpath("//td[@class='user_righttitle']//strong/text()")
            if isinstance(text, list) and text:
                title = element.xpath("//td[@class='user_righttitle']//strong/text()")[0]
            else:
                title = text
            category_first = element.xpath("//a[@class='LinkPath']")[-2].text
            category_second = element.xpath("//a[@class='LinkPath']")[-1].text
            poet, poem_name = title_pattern.findall(title)[0]
            content_list = element.xpath("//td[@class='main_tdbg_575']/table[2]//text()")
            content_results = list()
            for i in content_list:
                if i.strip():
                    content_results.append(i.strip().replace('"', "'"))
            contents = dict(
                poem_name=poem_name,
                poet=poet,
                category_first=category_first,
                category_second=category_second,
                content=content_results,
            )
            self._content_queue.put(contents)
            self._html_queue.task_done()

    def _save(self):
        while True:
            contents = self._content_queue.get()
            self._content_queue.task_done()
            client = DBClient()
            sql_temp = "insert into %TABLE%(%FIELDS%) values(%VALUES%)"
            sql = sql_temp.replace(
                '%TABLE%', DBConfig.TABLE
            ).replace(
                '%FIELDS%', ', '.join([
                    'category_first', 'category_second', 'poem_name', 'poet', 'content'
                ])
            ).replace(
                '%VALUES%', ','.join([
                    '"%s"' % contents['category_first'],
                    '"%s"' % contents['category_second'],
                    '"%s"' % contents['poem_name'],
                    '"%s"' % contents['poet'] or 'Unkown',
                    '"%s"' % '\r\n'.join(contents['content'])
                ])
            )
            print("Inserted: %s | %s | %s | %s" % (
                contents['category_first'],
                contents['category_second'],
                contents['poet'],
                contents['poem_name']
            ))
            client.exec(sql)
            client.close()



if __name__ == '__main__':
    poem = Poem()
    poem.run()
