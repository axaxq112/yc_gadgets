from glob import glob
import config
import requests
import re
import main

proxies = config.proxies

def getDanmu(oid):
    global proxies
    if oid == "":
        config.exit("[getDanmu]获取弹幕时传参OID为空,已退出")

    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + oid
    info_list=[]
    html = ""
    try:
        r = requests.get(url, timeout=5,proxies=proxies)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html = r.text
    except:
        config.exit("[getDanmu]爬取弹幕时出错，可能遇见了反爬问题: " + url)
    info_list = re.findall('<d p=".*?">(.*?)</d>', html)
    # print(info_list)
    danmuStr = ""
    for info in info_list:
        danmuStr = danmuStr + info + " | "
    #print(danmuStr)
    return danmuStr