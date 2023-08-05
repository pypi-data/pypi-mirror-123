# -*- coding: utf8 -*-
import json
from datetime import datetime
from datetime import timedelta
import traceback
import base64
import time
import hashlib
from threading import Timer

import pymysql

import urllib3
urllib3.disable_warnings()
import requests

reqs = requests.session()
reqs.keep_alive = False
reqs.adapters.DEFAULT_RETRIES = 5

from download_center.new_spider.downloader import config  # py3
import sys


def util_md5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


class Downloader(object):
    """
    通用下载器
    """

    def __init__(self, set_mode='db', get_mode='db', store_type=5):     # 兼容
        self.t = Timer(60*10, self.reset_ip)
        pass

    def reset_ip(self):
        """
        当接口调用失败后，重新ping以下网络情况，并更新接口地址
        :return:
        """
        try:
            ip_type = 1 if config.ping(config.DOWNLOADER_CENTER_INNER_IP) else 2
            if ip_type == 2 :
                self.t.start()
            else:
                self.t.cancel()
            response = reqs.post(config.TASK_SCHEDULER_IP.format(config.IP_HOST), data={"type": ip_type}, timeout=config.REQUEST_TIMEOUT)
            config.downloader_ip = str(response.content).strip()
        except:
            time.sleep(60)
            print(traceback.format_exc())

    def downloader_add_black_ip(self, ip, type, expire_time=6):
        try:
            data = {"ip": ip, "type": type, "expire_time": expire_time}
            reqs.post(config.ADD_BLACK_IP.format(config.downloader_ip), data=data, timeout=config.REQUEST_TIMEOUT)
            return True
        except:
            print(traceback.format_exc())
            return False

    def get_task_id(self,urls,config_dict=dict()):
        try:
            if len(config_dict)==0:
                name = "task_{}".format(str(round(time.time() * 1000)))
                config_dict = {"name": name, "concurrency": 50, "priority": 2, "crawl_once": 3}
            for i in range(2):
                try:
                    r = reqs.post(config.VALIDATE_ACCOUNT_URL, data=config_dict, timeout=config.REQUEST_TIMEOUT)
                    rdata = json.loads(r.text)
                    if rdata['success']:break;
                except:
                    time.sleep(config.REQUEST_RETYR_SLEEP)
                    rdata = {'success': False, 'message': str(traceback.format_exc())}
                if not rdata["success"]:continue;
        except:
            rdata = {'success': False, 'message': str(traceback.format_exc())}
            print("datetime: {}; error: {}".format(str(datetime.now()), str(traceback.format_exc())))
        return rdata

    # name, concurrency,priority,crawl_once
    def validate_accout(self, user="", password=""):
        try:
            ip_type = 1 if config.ENVIR == 'inner' else 2
            data = {"user": user, "password": password, 'type': ip_type}
            for i in range(2):
                try:
                    r = reqs.post(config.VERUFY_NEW_USER_URL, data=data, timeout=config.REQUEST_TIMEOUT)
                    rdata = json.loads(r.text)
                    break
                except:
                    time.sleep(config.REQUEST_RETYR_SLEEP)
                    # print(traceback.format_exc())
                    rdata = {'status': 0,'msg':'login failure'}

            if rdata["status"] == 0:
                print(rdata["msg"])
                return False
            else:
                config.downloader_ip = rdata["ip"]
                return (rdata["user_id"],rdata["task_id"])
        except:
            print("datetime: {}; error: {}".format(str(datetime.now()), str(traceback.format_exc())))
            return False

    def get_new_urls(self,request):
        new_urls = []
        for task in request.urls:
            t = json.loads(task)
            t['tid'] = request.task_id
            new_urls.append(json.dumps(t))
        return new_urls

    def set(self, request):
        """
        放任务
        Returns:
            正常: 返回字典，key值为每个url，value值0（失败）、  1（成功） 其它失败
            出错: 0 参数问题  -2 地域问题  -1 错误 1 正常

        請求異常 超時  返回正常， 其它根據返回狀態
        """
        try:
            new_urls = self.get_new_urls(request)
            try:
                data = {"user_id": request.user_id,
                        "task_id": request.task_id,
                        "urls": json.dumps(new_urls),
                        "config": request.config,
                        }
            except:
                print('new_urls = {}'.format(new_urls))

            r = {}
            for i in range(3):
                try:
                    rdata = reqs.post(config.DOWNLOADER_SENDTASK.format(config.IP_HOST), data=data, timeout=config.REQUEST_TIMEOUT)
                    r = json.loads(rdata.text)
                    break
                except:
                    time.sleep(config.REQUEST_RETYR_SLEEP)
                    r = {'success': False, 'message': 'set task failure'}
        except Exception:
            print("datetime: {}; error: {}".format(str(datetime.now()), str(traceback.format_exc())))
            time.sleep(config.REQUEST_RETYR_MAX_SLEEP)
            r = {'success': False, 'message':str(traceback.format_exc())}
        return r
            # self.reset_ip()
            # for url in request.urls:
            #     if 'unique_key' in url.keys():
            #         md5 = util_md5(pymysql.escape_string(url['url']) + str(url['unique_key']))
            #     else:
            #         md5 = util_md5(pymysql.escape_string(url['url']))
            #     url['unique_md5'] = md5
            # return -1

    def get(self,task_id):# page=1
        """求特定url的结果
        模式，redis-
        向下载中心请>直接查询redis数据库，db->直接查询数据库，http->通过http接口查询
        Args:
            request: SpiderRequest对象
        """
        try:
            for i in range(5):
                try:
                    rdata = reqs.post(config.DOWNLOADER_GETRESULT.format(config.IP_HOST), data={"task_id": task_id}, timeout=config.REQUEST_TIMEOUT)
                    res = json.loads(rdata.text)
                except Exception:
                    res = {'success': False,'msg':'reqs failure'}
                    print(str(traceback.format_exc()))
                    continue
                if res['success'] and len(res['results'])>0:
                    break
                else:
                    time.sleep(3)
            if res['success'] :
                return res
            else:
                print("get error msg: {}".format(res))
                return {"success":False,'msg':'reqs failure'}
        except Exception:
            return {"success":False,"msg":str(traceback.format_exc())}

    # 销毁task_id
    def destroy_task_id(self,request):
        try:
            data = {"task_id": request.task_id}
            for i in range(3):
                try:
                    rdata = reqs.post(config.DOWNLOADER_DISCONNECT.format(config.IP_HOST), data=data, timeout=config.REQUEST_TIMEOUT)
                    res = json.loads(rdata.text)
                except Exception:
                    res = {'success': False,'msg':'reqs failure'}
                    print(traceback.format_exc())
                if res['success']:
                    break
                else:time.sleep(3);
        except Exception:
            return {"success":False,"msg":str(traceback.format_exc())}


class SpiderRequest(object):

    __slots__ = ['user_id','urls','task_id','config','response_list','all_request_num']    # save memory

    def __init__(self, user_id=None, urls=list(),task_id=None,config=dict(),response_list=[]):
        self.user_id = user_id
        self.urls = urls
        self.config= config
        self.task_id= task_id
        self.response_list= response_list
        self.all_request_num = len(self.urls)


def main():
    spider = Downloader()
    # spider.validate_accout(user="test", password="Welcome#1")
    # spider.validate_accout(user="sunxiang", password="sxspider")
    spider.reset_ip()
    # req = SpiderRequest()
    # print(spider.get(req))

    # spider.downloader_add_black_ip("fihf", '11', expire_time=6)
    print(config.downloader_ip)


if __name__ == '__main__':
    main()


