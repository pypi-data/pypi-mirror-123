# -*- coding: utf8 -*-
import dis
import hashlib
from download_center.new_spider.downloader.downloader import Downloader
from download_center.new_spider.downloader.downloader import SpiderRequest
from download_center.new_spider.downloader.html_local_downloader import HtmlLocalDownloader
from download_center.new_spider.util.util_useragent import UtilUseragent
from multiprocessing import Process, Manager
from queue import Queue
from queue import Empty
from threading import Thread,Lock
import time
import traceback
import objgraph
from datetime import datetime
import uuid
from prettytable import PrettyTable
import sys
import json
lock = Lock()
class BaseSpider(object):
    """
    基本的爬虫类
    该爬虫维护四个队列：待发送队列sending_queue、已发送队列sended_queue
    取回结果队列response_queue、待存储队列store_queue
    发送的对象统一封装成SpiderRequest对象
    启动时，通过start_requests方法构造一批待发送的SpiderRequest对象送到待发送队列里面
    发送线程send_requests依次从sending_queue队列取值并发送，获取的结果通过deal_request_results来处理
    如果发送成功，将SpiderRequest对象送入已发送队列sended_queue，如果发送失败则重新回到待发送队列sending_queue
    取结果线程get_response依次从sended_queue队列取值并发送，获取的结果放至取回结果队列response_queue，
    deal_response_results从取回结果队列response_queue取出来处理，处理结束后可把结果放至待存储队列store_queue异步存储，也可在
    deal_response_results直接调用stores的存储方法直接存储
    如果抓取成功，将对应结果存入数据库，如果发送失败则重新回到已发送队列sended_queue
    """

    def __init__(self, remote=True):
        self.remote = remote
        self.pc_user_agents = UtilUseragent.get()
        self.mb_user_agents = UtilUseragent.get(type='MOBILE')
        self.sending_queue = Queue()
        self.sended_queue = Queue()
        self.response_queue = Queue()
        self.store_queue = Queue()
        self.task_id = ''
        self.user_id = 0
        self.stores = self.get_stores()
        self.downloader = self.get_downloader()
        self.sended_queue_max = 5000    # sended_queue 最大值
        self.response_queue_max = 1500  # response_queue 最大值
        self.store_queue_max = 2000     # store_queue 最大值
        self.url_repeat = True          # 默认重复的url重发 false 不重发
        self.downloader_ip = None
        self.thread_wait = 0            # 线程等待时间
        self.rst_num = 0                # 结果获取的数量
        self.send_num = 0               # 已发送数量

    def get_user_password(self):
        """
        设置用户名和密码，由子类实现。用于爬取前验证是否合法
        """
        raise NotImplementedError()

    def validate_user(self):
        """
        验证用户
        """
        if self.remote:
            user, password = self.get_user_password()
            user_id,task_id = self.downloader.validate_accout(user=user, password=password)
            if user_id:
                self.user_id = user_id
                self.task_id = 'pt_sz_05'
                print("user: {}; password: {} user validate success".format(user, password))
            else:
                raise RuntimeError('用户验证失败')
                sys.exit()
        else:
            pass


    def get_downloader(self):
        """
        设置下载器类型，默认为Downloader
        Return:
            SpiderDownloader
        """
        if self.remote:
            return Downloader()
        else:
            print("local downloader")
            return HtmlLocalDownloader()

    def start_requests(self):
        """
        初始化待发送请求队列，由子类实现。拼装一串SpiderRequest对象并送到sending_queue队列中
        """
        raise NotImplementedError()

    def is_finish(self):
        """
        根据相关队列是否全都为空来判断任务处理结束
        """
        return self.sending_queue.empty() and self.sended_queue.qsize() == 0  and self.response_queue.empty() and self.store_queue.empty()

    def send_requests(self , max_idle_time):
        """
        发送请求。将sending_queue队列中的SpiderRequest对象通过downloader发送到下载中心
        """
        start_time = time.time()
        while True:
            try:
                if self.sended_queue.qsize() < self.sended_queue_max and self.response_queue.qsize() < self.response_queue_max:
                    request = self.sending_queue.get(timeout=1)
                    if request.user_id is None:
                        request.user_id = self.user_id

                    #taskId 为固定分配
                    if request.task_id is None:
                        request.task_id = self.task_id
                        request.response_list = []

                    # task_id_status = self.downloader.get_task_id(request.urls,request.config)
                    # if task_id_status['success']:
                    #     request.task_id = task_id_status['task_id']
                    #     request.response_list = []
                    # else:
                    #     print('get task_id error ')
                    #     sys.exit()

                    results = self.downloader.set(request)
                    # 记录一下获发送了多少结果
                    self.send_num += len(request.urls)
                    # print('发送任务数：')
                    # print(self.send_num)

                    if results['success']:
                        for tempUrl in  request.urls:
                            self.sended_queue.put(json.loads(tempUrl)['uid'])
                    else:
                        print('send parameters error urls: {}'.format(request.urls))

                    start_time = time.time()
                    self.send_wait()
                else:
                    time.sleep(10)
            except Empty:
                if max_idle_time == -1:
                    pass
                elif start_time + max_idle_time < time.time():
                    if self.is_finish():
                        break
                time.sleep(10)
            except Exception:
                print(traceback.format_exc())


    def send_wait(self):
        """
        发送等待, 控制发往下载中心的速率
        """
        if self.thread_wait != 0:
            time.sleep(self.thread_wait)
        else:
            if self.sended_queue.qsize() > 8000:
                time.sleep(10)
            elif self.sending_queue.qsize() < 1000:
                time.sleep(1)
            else:
                time.sleep(0.1)

    def get_wait(self):
        """
        获取结果等待, 控制发往处理队列的速率
        """
        if self.thread_wait != 0:
            time.sleep(self.thread_wait)
        else:
            if self.response_queue.qsize() > 4000:
                time.sleep(5)
            elif self.sended_queue.qsize() < 2000:
                time.sleep(1)
            else:
                time.sleep(0.1)

    def get_response(self, max_idle_time):
        """
        获取url爬取结果。将sended_queue队列中的SpiderRequest对象通过downloader到下载中心去获取抓取到的html
        """
        start_time = time.time()
        while True:
            try:
                if self.response_queue.qsize() < self.response_queue_max:
                    # request = self.sended_queue.get(timeout=1)
                    # 新的方法直接根据task_id获取任务
                    results = self.downloader.get(self.task_id)
                    self.response_queue.put(results)  # 存在多个结果
                    start_time = time.time()
                    self.get_wait()  # wait confirm
                else:
                    time.sleep(5)
            # try:
            #     if self.response_queue.qsize() < self.response_queue_max:
            #         # request = self.sended_queue.get(timeout=1) # task_id,user_id,urls
            #         # 新的方法直接根据task_id获取任务
            #         results = self.downloader.get(self.task_id)
            #
            #
            #         if results['success'] :
            #             result_num = len(results.get('results',[]))
            #             result_list = results.get('results', '')
            #             for res in result_list:
            #                 self.response_queue.put(res) #将结果循环存入队列
            #
            #                 # res_dict = json.loads(res)
            #                 # print(res_dict['uid'])
            #
            #             # 记录一下获取到了多少结果
            #             self.rst_num += result_num
            #             print('获取结果数：')
            #             print(self.rst_num)
            #
            #         start_time = time.time()
            #         self.get_wait()     # wait confirm
            #     else:
            #         time.sleep(5)
            except Empty:
                if max_idle_time == -1:
                    pass
                elif start_time + max_idle_time < time.time():
                    if self.is_finish():
                        break
                time.sleep(5)
            except Exception:
                print(traceback.format_exc())

    def deal_response(self,max_idle_time):
        """
        从结果队列response_queue中取出结果进行处理
        """
        start_time = time.time()
        while True:
            try:
                if self.store_queue.qsize() < self.store_queue_max and self.response_queue.qsize() > 0:
                    results = self.response_queue.get(timeout=1)
                    try:
                        self.deal_response_results_v2(results, self.stores)
                        # self.cheak_response_list(request)
                    except Exception:
                        print(traceback.format_exc())
                    start_time = time.time()
                else:
                    time.sleep(10)
            except Empty:
                if max_idle_time == -1:
                    pass
                elif start_time + max_idle_time < time.time():
                    if self.is_finish():
                        break
                time.sleep(10)
            except Exception:
                print(traceback.format_exc())

    def store_results(self, max_idle_time):
        """
        从store_queue里面取出待存储的数据进行存储
        """
        start_time = time.time()
        while True:
            try:
                results = self.store_queue.get(timeout=1)
                self.to_store_results(results, self.stores)
                start_time = time.time()
            except Empty:
                if max_idle_time == -1:
                    pass
                elif start_time + max_idle_time < time.time():
                    if self.is_finish():
                        break
                time.sleep(10)
            except Exception:
                print(traceback.format_exc())

    def to_store_results(self, results, stores):
        """
        存储结果，由子类实现。
        Args:
            results:处理response后的结果
            stores:list，可能会用到的存储器（SpiderStore）列表
        """
        pass

    def get_stores(self):
        """
        设置存储器，供deal_response_results调用
        Return:
            list,成员为SpiderStore对象
        """
        stores = list()
        return stores

    #垃圾的服务器端接口，让我们必须循环队列所有任务
    def deal_response_results(self, results, stores):
        if results['success']:
            result_list = results.get('results','')
            if len(result_list):
                #循环判断sended_queue里的数据是否处理完成，如果结果在sended的list，则删除，如果list里的request对象里的urls为空，则删除当前request
                for request in self.sended_queue:

                    # 如果当前requets的urls没有记录了，则删除当前request
                    if len(request.urls) == 0:
                        self.sended_queue.remove(request)
                        break

                    for u in request.urls: # request.urls 列表
                        url_dict = json.loads(u)  # 发送的单个任务
                        uid = url_dict['uid']
                        if uid in json.dumps(result_list): #url的uid是否在结果里，在则说明是当前任务的结果
                            request.response_list.append(uid)
                            for res in result_list: #因为result_list一次最多获取10条，所以要循环处理。todo 需要升级
                                res_dict = json.loads(res)
                                if uid == res_dict['uid']:
                                    result = res_dict.get('body','')
                                    if result and res_dict['success']:
                                        self.deal_response_results_status(True, u, {'result': result}, request)
                                    else:
                                        self.deal_response_results_status(False, u, {'result': result}, request)

                                    # 如果当前结果ok,则删除但当前request的url。如果url为空，则删除当前request
                                    request.urls.remove(u)
                        # else:
                        #     urls.append(u)
            # else:
            #     没有结果，则继续循环获取
                # pass
        # else:
        #     pass
            # 如果结果获取错误,也继续获取，无需处理
            # if self.cheak_response_list(request):
            #     return
            # request = SpiderRequest(urls=request.urls)
            # self.sending_queue.put(request)
        # if len(urls):
        #     request.urls = urls
        #     self.sended_queue.put(request)

    def deal_response_results_v2(self ,results, stores):
        if results['success']:
            result_list = results.get('results','')
            if len(result_list):
                for res in result_list:
                    res_dict = json.loads(res)
                    result = res_dict.get('body', '')
                    if result and res_dict['success']:
                        self.deal_response_results_status(True,  {'result': result})
                    else:
                        self.deal_response_results_status(False, {'result': result})

                    uid = self.sended_queue.get()

                    # print('标记删除：')
                    # print(uid)

    def cheak_response_list(self,request):
        if len(request.response_list) == request.all_request_num and request.all_request_num > 0:
            # self.downloader.destroy_task_id(request)
            # print('任务结束:task_id={}'.format(request.task_id))
            return True
        else:
            return False

    def reduction_url_dict(self,url_dict):
        """
            还原原始urls
        """
        new_url_dict = {}
        new_url_dict['url'] = url_dict['u']
        new_url_dict['type'] = 1
        new_url_dict['unique_key'] = url_dict['uid']
        if len(url_dict['debug']):
            for k,v in url_dict['debug'].items():
                new_url_dict[k] = v
        return new_url_dict

    def deal_response_results_status(self, task_status, result):
        """
            处理 task_status 是2,3的任务  重试返回数组， 若重试需切换headers内容需自行定义
        :param task_status:
        :param url:
        :param result:
        :param request:
        :return:
        """
        raise NotImplementedError()

    def record_log(self):
        """
        记录抓取日志，用于调整各个线程参数设置
        """
        while True:
            table = PrettyTable(["x", "y"])
            table.add_row(["datetime", str(datetime.now())])
            table.add_row(["sending_queue", self.sending_queue.qsize()])
            table.add_row(["sended_queue", self.sended_queue.qsize()])
            table.add_row(["response_queue", self.response_queue.qsize()])
            table.add_row(["store_queue", self.store_queue.qsize()])
            table.reversesort = True
            print(table)
            del table
            # objgraph.show_most_common_types()
            time.sleep(10)
            if self.is_finish():
                break

    @staticmethod
    def get_unique_key():
        """
        生成唯一标识
        :return:
        """
        return str(uuid.uuid1())

    def add_black_ip(self, ip, type, expire_time=6):
        """
        记录IP黑名单
        使用黑名单功能需在发送请求时在config设置param参数中配置任务类型
        config : {param: {'task_type': 1}}
        Args:
            ip: IP地址
            type: 指定任务类型有效
            expire_time: 超时时间(小时)
        """
        self.downloader.downloader_add_black_ip(ip, type, expire_time=expire_time)

    def clear_task_pool(self):
        """
        清空当前用户已发往下载中心的任务
        :return:
        """
        pass

    def after_deal_response(self, request, results):
        """
        抓取结果的处理逻辑后的后续操作，按需使用，默认不作任何操作
        :param request:
        :param results:
        :return:
        """
        pass

    @staticmethod
    def retry(u, count):
        retry_urls = list()
        if u.get("re_send", 0) < int(count):
            u["re_send"] = u.get("re_send", 0) + 1
            retry_urls.append(u)
        else:
            print("conf_search_count > {};url: {}".format(count, u["url"]))
        return retry_urls

    def md5_url(self,url):
        md = hashlib.md5()  # 创建md5对象
        md.update(url.encode(encoding='utf-8'))
        return md.hexdigest()

    def run(self, send_num=0, get_num=0, deal_num=0, store_num=0,
            send_idle_time=600, get_idle_time=600,
            deal_idle_time=600, store_idle_time=600, record_log=False, spider_count=0):
        """
        爬虫启动入口
        Args:
            send_num:发送请求线程数，默认为0
            get_num:获取结果线程数，默认为0
            deal_num:处理结果线程数，默认为0
            store_num:存储结果线程数，默认为0
            send_idle_time:发送请求线程超过该时间没有要发送的请求就停止，-1永不停止
            get_idle_time:获取结果线程超过该时间没有要获取的结果就停止，-1永不停止
            deal_idle_time:处理结果线程超过该时间没有要处理的结果就停止，-1永不停止
            store_idle_time:存储结果线程超过该时间没有要存储的结果就停止，-1永不停止
            record_log:定时记录各个队列大小，便于分析抓取效率
            spider_count: 设置每小时发送量
        """
        self.validate_user() #
        thread_start = Thread(target=self.start_requests)
        thread_start.start()

        if send_num == 0:        # 用户自行配置
            if spider_count == 0:
                print("not set send_num and spider_count")
                sys.exit()
            else:
                send_num = 5
                get_num = 7
                if deal_num == 0:
                    deal_num = 5
                if store_num == 0:
                    store_num = 5
                self.thread_wait = round(3600/(float(spider_count)/send_num), 2)

        print("send_num: {}; get_num: {}; deal_num: {}; store_num: {}; spider_count: {}".format(send_num, get_num, deal_num, store_num, spider_count))
        threads = list()
        for i in range(0, send_num):
            threads.append(Thread(target=self.send_requests, args=(send_idle_time,)))
        with Manager() as manager:
            threads.append(Thread(target=self.get_response, args=(get_idle_time,)))
        for i in range(0, deal_num):
            threads.append(Thread(target=self.deal_response, args=(deal_idle_time,)))
        for i in range(0, store_num):
            threads.append(Thread(target=self.store_results, args=(store_idle_time,)))

        if record_log:
            thread = Thread(target=self.record_log)
            thread.setDaemon(True)
            threads.append(thread)
        for thread in threads:
            thread.start()
