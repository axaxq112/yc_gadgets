from glob import glob
import config
import requests
import re
import main

proxies = config.proxies

def getReply(avID):
    global proxies
    if avID == "":
        config.exit("[getReply]获取视频频率时时传参avID为空,已退出")

    url =  'https://api.bilibili.com/x/v2/reply/main?mode=3&next=0&oid=这边是av号&plat=1&type=1'
    info_list=[]
    html = ""
    try:
        r = requests.get(url, timeout=5,proxies=proxies)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html = r.text
    except:
        config.exit("[getReply]爬取评论时出错，可能遇见了反爬问题: " + url)
    return html