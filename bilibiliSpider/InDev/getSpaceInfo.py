from glob import glob
import config
import requests
import re
import main

proxies = config.proxies

def getSpaceInfo(mid):
    global proxies
    if mid == "":
        config.exit("[getSpaceInfo]获取用户空间时传参mid为空,已退出")

    url =  'https://api.bilibili.com/x/space/top/arc?vmid=' + mid + '&jsonp=jsonp'
    html = ""
    try:
        r = requests.get(url, timeout=5,proxies=proxies)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html = r.text
    except:
        config.exit("[getSpaceInfo]爬取用户空间信息时出错，可能遇见了反爬问题: " + url)
    return html