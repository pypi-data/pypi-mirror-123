# -*- coding: utf-8 -*-
"""
@Time:2020/3/10 14:39
@Author:wuwenjie
"""
from platform import system as system_name  # Returns the system/OS name
from os import system as system_call  # Execute a shell command


# 下载中心redis
DOWNLOADER_CENTER_REDIS = {
    'outer': {
        'host': '115.159.3.51',
        'port': 53189,
        'db': 0,
        'password': '&redisd0o#2@1951'
    },
    'inner': {
        'host': '10.154.199.106',
        'port': 53189,
        'db': 0,
        'password': '&redisd0o#2@1951'
    }
}


def ping(ip):
    try:
        if system_name().lower() == "windows":
            return True
        else:
            return False
    except:
        print("取cookie异常")

if ping(DOWNLOADER_CENTER_REDIS['outer']['host']):
    ENVIR = 'outer'
else:
    ENVIR = 'inner'
