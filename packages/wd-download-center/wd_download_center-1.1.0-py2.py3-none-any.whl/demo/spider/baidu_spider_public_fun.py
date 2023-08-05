# -*- coding: utf8 -*-
import json
import os
import re
import sys
import random
import time
import base64
import traceback
from http import cookiejar
from urllib.request import Request, HTTPCookieProcessor, build_opener

from lxml.html import fromstring
import urllib.parse
from util.domain_urllib import SeoDomain
from lxml import etree
from util.get_baidu_cookie import baiduCookie

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'spider_service_system'))


class BaiduSpiderPublicFun(object):
    """
    解析百度移动端，获取片名，real_url,rank
    """

    def __init__(self):
        super(BaiduSpiderPublicFun, self).__init__()
        self.baidu_cookie = baiduCookie()
        self.sx_FindDomain = SeoDomain()

    # 获取移动端ua
    def get_mobile_useragent(self):
        mobile_useragent_list = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/533.36",
            "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-CN; Letv X501 Build/DBXCNOP5501304131S) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.0.800 U3/0.8.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; Letv X501 Build/DBXCNOP5501304131S) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 5.1.1)",
            "Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; N5117 Build/JLS36C) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baiduboxapp/7.0 (Baidu; P1 4.3)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/13D15 UCBrowser/10.9.15.793 Mobile",
            "Mozilla/5.0 (iPhone 6p; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.7 Mobile/13D15 Safari/8536.25 MttCustomUA/2",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1",
            "Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-S7572 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; SM-J3109 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.6 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; Coolpad 8297-T01 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.6 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; MX4 Pro Build/LMY48W) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.0.800 U3/0.8.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; Android 5.1; m2 note Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.114 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; m2 note Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.10.788 U3/0.8.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m2 note Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.6 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; CHM-CL00 Build/CHM-CL00) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baiduboxapp/7.1 (Baidu; P1 4.4.4)",
            "Mozilla/5.0 (Linux; Android 5.0.1; HUAWEI GRA-TL00 Build/HUAWEIGRA-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 MxBrowser/4.5.9.3000",
            "Mozilla/5.0 (Linux; Android 5.0.1; HUAWEI GRA-CL00 Build/HUAWEIGRA-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 5.0.1)",
            "Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 5.0.2)",
            "Mozilla/5.0 (Linux; Android 4.4.4; Che1-CL10 Build/Che1-CL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 4.4.4)",
            "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; HUAWEI P6-C00 Build/HuaweiP6-C00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.3; R7007 Build/JLS36C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 4.3)",
            "Mozilla/5.0 (Linux; Android 5.1.1; KIW-CL00 Build/HONORKIW-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.1 baidubrowser/7.1.12.0 (Baidu; P1 5.1.1)",
        ]
        return random.choice(mobile_useragent_list)

    # 获取pc端ua
    def get_pc_useragent(self):
        pc_useragent_list = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
            "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        ]
        return random.choice(pc_useragent_list)

    # 获取pc端请求头
    def get_pc_headers(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.baidu.com/',
            'Host': 'www.baidu.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            "Sec-Fetch-Dest": "document",
            'User-Agent': self.get_pc_useragent(),
            # "Cookie": self.get_cook("1"),
            # "Cookie": """BAIDUID=637AACB9795F74E815557140EF106D72:SL=0:NR=10:FG=1; BIDUPSID=6E9B6D7E95E1DF2445E6B5E61E8C1F4A; PSTM=1602650706; BD_UPN=13314752; BDUSS=lVxMkhSZWt0QUFJWTZBYVFRY1VmbDluMEpvdXlOWFZPZERDUlkwV2FtZVRNYTVmSVFBQUFBJCQAAAAAAAAAAAEAAACofMPNaXdlc3RlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJOkhl-TpIZfM; H_WISE_SIDS=161925_161576_163320_163390_156288_161252_159614_162914_160938_163304_162372_159383_162046_159936_161422_162176_160878_161125_161419_161969_127969_161770_160764_1617…196419210_218.4.33.186_c29215f7; yjs_js_security_passport=b744b3744a7648346c7ceb4a6157c309a94632ae_1608196420_js; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; BDRCVFR[Fc9oatPmwxn]=G01CoNuskzfuh-zuyuEXAPCpy49QhP8; BD_HOME=1; sug=3; sugstore=1; ORIGIN=2; bdime=0; BA_HECTOR=a52l0gah04a40l81891ftmhl10q; H_PS_645EC=18af1BkU3EESaFTiCdi3Qeb3LsbCy9oMngNI%2BhS348qTqWemlp7LIZG5TiYtOwHIalgE; BDSVRTM=229; COOKIE_SESSION=15520_0_3_3_12_4_0_0_2_3_1_0_0_0_4_0_1608190468_0_1608205984%7C9%237074_8_1607426975%7C7; WWW_ST=1608206027986""",
        }
        return headers

    def get_mb_cookie(self):
        cookies = None
        try:
            cookie_jar = cookiejar.CookieJar()
            request = Request('https://m.baidu.com/tc?tcreq4log=1', headers={})
            handlers = [HTTPCookieProcessor(cookie_jar)]
            opener = build_opener(*handlers)
            opener.open(request, timeout=10)
            for cookie in cookie_jar:
                if cookie.name == 'BDORZ':
                    cookies = 'BDORZ=' + cookie.value
                    break
        except Exception:
            pass
        return cookies

    # 获取移动端请求头
    def get_mb_headers(self):
        headers = {
            'Host': 'm.baidu.com',
            'User-Agent': random.choice(self.get_mobile_useragent()),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://m.baidu.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            # 'Cookie': self.get_cook("2"),
            # 'Cookie': self.get_mb_cookie(),
        }
        return headers

    # 获取公用库百度cookie
    def get_cook(self, device):
        """
        获取有效的cookie
        :return:
        """
        if device == '1':
            key_name = 'pc'
        else:
            key_name = 'mb'
        for i in range(2):
            if self.baidu_cookie.totalCookies(key_name=key_name) > 0:
                cookie = str(self.baidu_cookie.getLastCookies(key_name=key_name)[0], encoding="utf-8")
                return cookie
            else:
                print('no cookie')
                return 'BAIDUID={}:FG=1'.format(time.time())
        return ''

    # 拆解任务url
    def judge_url(self, ckurl):
        """
        判断url是否是一个json字符串，如果是返回一个由url组成的list
        :param ckurl:
        :return:
        """
        url_list = list()
        if ckurl.startswith("["):
            try:
                ckurl = ckurl.replace("\\'", "\"")
                url_list = json.loads(ckurl)
            except:
                print(traceback.format_exc())
                print("-------------")
                print(ckurl)
                url_list.append(ckurl)
        else:
            ckurl = ckurl.replace("'", "\"")
            url_list.append(ckurl)
        return url_list

    # 格式化pc端入库html
    def format_pc_html_save(self, html):
        html = html.replace("https://www.baidu.com/img/flexible/logo/pc/result.png",
                            "img/flexible/logo/pc/result.png") \
            .replace("//www.baidu.com/img/flexible/logo/pc/result.png", "img/flexible/logo/pc/result.png") \
            .replace('https://www.baidu.com/img/flexible/logo/pc/result@2.png', "img/flexible/logo/pc/result@2.png") \
            .replace('//www.baidu.com/img/flexible/logo/pc/result@2.png', "img/flexible/logo/pc/result@2.png")
        return str(base64.b64encode(html.encode(encoding="utf-8")), encoding="utf-8")

    # 格式化移动端入库html
    def format_mb_html_save(self, html):
        html = html.replace('position: fixed; display: flex; bottom: 0px; left: 0px; z-index: 300;', 'display:none;') \
            .replace('https://www.baidu.com/img/flexible/logo/logo_web.png', "img/flexible/logo/logo_web.png") \
            .replace('//www.baidu.com/img/flexible/logo/logo_web.png', "img/flexible/logo/logo_web.png")
        html = self.format_mb_img_src(html)
        return str(base64.b64encode(html.encode(encoding="utf-8")), encoding="utf-8")

    def format_mb_img_src(self, html):
        try:
            img_div= '<div style="display:none;">'
            img_all_list = []
            img_list = []
            lazy_img_list = []
            tree = fromstring(html)
            images = tree.xpath("//div[@id='results']//img")

            # images = []
            # images += tree.xpath("//div[@id='results']//div[@srcid='www_normal']//img")
            # images += tree.xpath("//div[@id='results']//div[@srcid='www_zhidao_normal']//img")
            # images += tree.xpath("//div[@id='results']//div[@srcid='lego_tpl']//img")
            # images += tree.xpath("//div[@id='results']//div[@srcid='sp_purc']//img")
            # images += tree.xpath("//div[@id='results']//div[@srcid='vid_hor']//img")[0:2]
            # images += tree.xpath("//div[@id='results']//div[@srcid='image_normal_tag']//img")[0:5]
            # images += tree.xpath("//div[@id='results']//div[@srcid='sigma_celebrity_rela']//img")[0:3]

            for idx, image in enumerate(images):
                try:
                    src = images[idx].attrib['src']
                    if src not in img_all_list:
                        img_list.append(src)
                        img_all_list.append(src)
                except:
                    pass

                try:
                    src = images[idx].attrib['data-lazy-src']
                    if src not in img_all_list:
                        lazy_img_list.append(src)
                        img_all_list.append(src)
                except:
                    pass

            if img_list:
                for img_item in img_list:

                    new_src = '/showpic.php?url=' + urllib.parse.quote(img_item)
                    img_div += '<img src="{}">'.format(new_src)
                    html = html.replace(img_item, new_src)
                    img_item = img_item.replace('&', '&amp;')
                    html = html.replace(img_item, new_src)

            if lazy_img_list:
                for img_item in lazy_img_list:

                    new_src = '/showpic.php?url=' + urllib.parse.quote(img_item)
                    img_div += '<img src="{}">'.format(new_src)
                    html = html.replace(img_item, new_src)
                    img_item = img_item.replace('&', '&amp;')
                    html = html.replace(img_item, new_src)

                    data_lazy_src = 'data-lazy-src="{}"'.format(img_item)
                    data_lazy_src_new = 'src="{}"'.format(new_src)
                    html = html.replace(data_lazy_src, data_lazy_src_new)

            img_div += '</div>'

            # 塞入图片
            old_head = '<div id="page-hd" class="se-page-hd">'
            new_head = '<div id="page-hd" class="se-page-hd">'+img_div
            html = html.replace(old_head, new_head)

            # 塞入load标识
            load_img = '''<script>window.onload=function(){document.body.setAttribute('id', 'img_load_success')}</script>'''
            html = html.replace('</body>', load_img+'</body>')

            return html
        except:
            return html

    def format_mb_img_src_01(self, html):
        try:
            img_list = []
            lazy_img_list = []
            tree = fromstring(html)
            images = tree.xpath("//div[@id='results']//img")
            for idx, image in enumerate(images):
                try:
                    src = images[idx].attrib['src']
                    img_list.append(src)
                except:
                    pass

                try:
                    src = images[idx].attrib['data-lazy-src']
                    lazy_img_list.append(src)
                except:
                    pass

            if img_list:
                for img_item in img_list:
                    new_src = '/showpic.php?url=' + urllib.parse.quote(img_item)
                    img_item = img_item.replace('&', '&amp;')
                    html = html.replace(img_item, new_src)

            if lazy_img_list:
                for img_item in lazy_img_list:
                    new_src = '/showpic.php?url=' + urllib.parse.quote(img_item)
                    img_item = img_item.replace('&', '&amp;')
                    data_lazy_src = 'data-lazy-src="{}"'.format(img_item)
                    data_lazy_src_new = 'src="{}"'.format(new_src)
                    html = html.replace(data_lazy_src, data_lazy_src_new)

            return html
        except:
            return html


    # 判断pc端dom元素是否异常
    def check_pc_dom_is_error(self, html):
        if html.find("</html>") < 0 or html.find('id="wrap"') >= 0 or (
                "<title>百度App</title>" in html and "拦截通用" in html) or (
                "<title>百度安全验证</title>" in html and "百度安全验证" in html) or html.find('页面不存在_百度搜索') >= 0 or html.find(
            'id="container"') < 0 or html.find('id="content_left"') < 0 or html.find('<title>') < 0:
            return True
        else:
            return False

    # 判断移动端dom元素是否异常
    def check_mb_dom_is_error(self, html):
        if html.find("</html>") < 0 or html.find('id="results"') < 0 or (
                "<title>百度App</title>" in html and "拦截通用" in html) or (
                "<title>百度安全验证</title>" in html and "百度安全验证" in html) or html.find('页面不存在_百度搜索') >= 0 \
                or html.find('<title>') < 0:
            return True
        else:
            return False

    def format_source(self, conf_district_id):
        """
        'source':  #  1全国 2：苏州ip 3：桌面软件
        :return:
        """
        try:
            if conf_district_id == 0:
                return 1
            elif conf_district_id == 3:
                return 2
            return 1
        except Exception:
            return 1

    # 拆分知乎id
    def formate_zhihu_id(self, url):
        try:
            return re.match(r".*zhihu.com/question/(\d+)?/*", str(url)).group(1)
        except:
            return url

    # 拆分百科百科id
    def formate_baike_id(self, url):
        try:
            if "?" in url:
                baike_id = url.split("?")[0].split('/')[-1]
                return baike_id
            else:
                baike_id = url.split('/')[-1]
                return baike_id
        except:
            return ""

    # 拆分百度知道id
    def formate_baidu_zhidao_id(self, url):
        try:
            p = re.match(r".*question/(\d+)\.html?.*", str(url))
            teibaId = p.group(1)
            return teibaId
        except:
            return ''


    # 拆分贴吧id
    def formate_tieba_id(self, url):
        try:
            p = re.match(r".*kz=(\d+)&?.*", str(url))
            if not p:
                p = re.match(r".*p/(\d+)", str(url))
            teibaId = p.group(1)
            return teibaId
        except:
            return ''

    # 判断两个域名是不是相同主域 ， 匹配返回True
    def check_same_domain(self, device, task_url, baidu_real_url):
        try:
            if 'baidu.com' in baidu_real_url:
                task_url = self.sx_FindDomain.get_subdomain(task_url)
                baidu_real_url = self.sx_FindDomain.get_subdomain(baidu_real_url)
                if task_url == baidu_real_url:
                    return True
                else:
                    return False

            task_url = self.sx_FindDomain.sxGetDomain(task_url)
            baidu_real_url = self.sx_FindDomain.sxGetDomain(baidu_real_url)
            if task_url == baidu_real_url:
                return True
            return False
        except:
            return False

    # 判断标题是否匹配 ， 匹配返回True
    def match_title(self, device, task_title, baidu_title, real_url):
        try:
            if baidu_title.strip() == '' or task_title.strip() == '' or task_title is None or baidu_title.strip() is None:
                return False

            task_title = task_title.replace('?', '？').replace(',', '，')
            baidu_title = baidu_title.replace('?', '？').replace(',', '，')

            # 移动端 百度根据title完全匹配
            # if device == 'mb' and 'baidu.com' in self.sx_FindDomain.get_subdomain(real_url):
            if 'baidu.com' in self.sx_FindDomain.get_subdomain(real_url):
                if task_title.strip() == baidu_title.strip():
                    return True
                else:
                    return False

            # 判断完全相等
            if task_title.strip() == baidu_title.strip():
                return True
            # 去除 ...之后文本 后完全相等
            if task_title.split('...')[0].strip() == baidu_title.split('...')[0].strip():
                return True
            # 去除 _之后文本 后完全相等
            if task_title.split('_')[0].strip() == baidu_title.split('_')[0].strip():
                return True
            # 去除 -之后文本 后完全相等
            if task_title.split('-')[0].strip() == baidu_title.split('-')[0].strip():
                return True
            # 去除特殊符号后  长文本完全包含短文本，且从头开始
            sub_task_title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", task_title)
            sub_baidu_title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", baidu_title)
            if sub_task_title.startswith(sub_baidu_title) or sub_baidu_title.startswith(sub_task_title):
                return True

            return False
            # 引入相似度 todo

        except Exception:
            print(traceback.format_exc())
            return False


if __name__ == '__main__':
    a = BaiduSpiderPublicFun()

    a.get_mb_cookie()

    html = open('test_mb.html', 'r', encoding='utf-8').read()
    str_result = a.format_mb_html_save(html)
    str_result = str(base64.b64decode(str_result.encode("utf-8")), "utf-8")
    f = open('2.html', 'w', encoding='utf-8')
    f.write(str_result)
    f.close()
    pass
