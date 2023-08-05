# -*- coding: utf-8 -*-
import os
import os
import sys
import random
import base64
import traceback
import json

import time
import urllib.parse
from datetime import datetime

from download_center.new_spider.downloader.downloader import SpiderRequest
from download_center.new_spider.spider.basespider import BaseSpider
from download_center.util.util_log import UtilLogger
import hashlib
# 线上测试
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
from demo.extractor.baidu_extractor import BaiduExtractor
from demo.store.py_store_mysql_pool import StoreMysqlPool
from demo.spider.baidu_spider_public_fun import BaiduSpiderPublicFun

class DemoSpider(BaseSpider):
    def __init__(self, remote=True):
        super(DemoSpider, self).__init__(remote=remote)
        self.log = UtilLogger('DemoSpider', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_demo_spider'))
        self.ext = BaiduExtractor()
        db_225_ser = {
            # 'host': '10.154.94.79',  # 线上
            "host": "115.159.0.225",  # 线下
            'user': 'remote',
            'password': 'Iknowthat',
            'db': 'wj_data',
            'charset': 'utf8mb4',
        }
        self.db = StoreMysqlPool(**db_225_ser)
        self.task_table = 'download_client_test'
        self.baidu_spider_public_fun = BaiduSpiderPublicFun()
        self.data_sucess_num = 0
        self.data_error_num = 0

    def get_user_password(self):
        return 'test', 'Welcome#1'

    def start_requests(self):
        self.db.do("update {} set status= 0".format(self.task_table,))
        # while 1:
        for i in range(100):
            # rows = self.db.query('select id,keyword,device from {} where status=0 limit 2'.format(self.task_table))
            objUrls = []
            device = 1
            keyword = '汽车'
            change_state_ids = list()
            for x in range(1):
                headers = self.get_headers(device)
                if device==1:
                    kwd = urllib.parse.quote(keyword)
                    url = "https://www.baidu.com/s?wd={}".format(keyword + str(i) + str(x))
                else:
                    kwh = {'wd': keyword}
                    url = 'https://m.baidu.com/s?' + urllib.parse.urlencode(kwh)
                task = json.dumps({'hs':headers,'u':url,"et":0,'uid':self.md5_url(url),'debug':{'kid':i}}) # et=0
                objUrls.append(task)
                change_state_ids.append(str(id))

            request = SpiderRequest(urls=objUrls)
            self.sending_queue.put(request)
            # self.update_ids(change_state_ids)
            time.sleep(1)

    def get_headers(self,device):
        if device==1:
            return self.baidu_spider_public_fun.get_pc_headers()
        else:
            return self.baidu_spider_public_fun.get_mb_headers()

    def md5_url(self,url):
        md = hashlib.md5()  # 创建md5对象
        md.update(url.encode(encoding='utf-8'))
        return md.hexdigest()

    def get_stores(self):
        # 存储器
        stores = list()
        return stores

    def deal_response_results_status(self, response_status, result):
        # print('获取到结果 urls = {}'.format(urls))
        # task_id = json.loads(objUrl)['debug']['kid']
        if response_status:
            # self.db.update(self.task_table,{'id':task_id,'status':2},field='id')
            self.data_sucess_num += 1
            if self.data_sucess_num % 10 == 0 :
                print(self.data_sucess_num)
        else:
            # self.db.update(self.task_table,{'id':task_id,'status':-1},field='id')
            self.data_error_num += 1
            # print('失败的链接{},html = {}'.format(result['result']))
            self.log.info('抓取失败: {}')

    def update_ids(self,ids):
        try:
            sql = "update {}  set  status = 1 where id in ({}) ".format(self.task_table, ','.join(ids))
            self.db.do(sql)
        except:
            print(traceback.format_exc())


def main():
    spider = DemoSpider(remote=True)
    spider.run(1,1,1,1, record_log=True)   # 测试
    # spider.run(spider_count=1000, record_log=True)
    # spider.run(record_log=True)               # error


if __name__ == '__main__':
    main()
