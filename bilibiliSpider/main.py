import json
import time
import pymysql
import requests
from pymysql.converters import escape_string
import os
import subprocess
import sys

restartCommand = "open startMain.command"  #崩溃自重启命令，Mac调用command文件，Windows调用bat文件

timeFormat = '%Y-%m-%d %H:%M:%S' #时间格式
latestTxt = "latestAid.txt" #最近爬取的aid文件路径（用于崩溃自重启)
log_dir = 'logs' #日志目录

proxies = {'https': 'http://127.0.0.1:7890','http': 'http://127.0.0.1:7890'} #代理信息
proxies = {} #不设置代理

def sleepTime(hour, min, sec):
    return hour * 3600 + min * 60 + sec

def exit(contentStr = "",restartSecond = 0):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime(timeFormat, timeStruct)
    retStr = "[" + strTime + "] 程序退出原因:" + contentStr
    log_date = time.strftime("%Y-%m-%d", timeStruct)
    log_fn = log_dir + "/exitLog_" + log_date + ".txt"
    with open(log_fn, "a") as file:
        file.write(retStr + "\n")
    print(retStr)

    time.sleep(restartSecond) #等待重开间隔

    subprocess.Popen(restartCommand, shell=True) #调用重开命令,Windows下推荐用os.system()

    sys.exit(0) #退出程序运行


try:
    db = pymysql.connect(host='127.0.0.1', user='root', password='root', db='bilibiliSpider', port=3306)  #MySQL数据库连接配置
except Exception as e:
    reprStr = str(repr(e))
    restart_Second = sleepTime(0,0,10)
    exit("[main]链接MySQL数据库时出错，将在10秒后重启本程序",restart_Second)

create_table_videoContents_Sql = "CREATE TABLE IF NOT EXISTS `videoContents`( `id` int(30) unsigned NOT NULL AUTO_INCREMENT, `aid` int(255) DEFAULT NULL, `bvid` text CHARACTER SET utf8, `cid` int(255) DEFAULT NULL, `video_title` text, `video_desc` text, `video_tname` text, `video_pic` text CHARACTER SET utf8, `video_pubYear` int(10) DEFAULT NULL, `video_pubMonth` int(10) DEFAULT NULL, `video_pubDay` int(10) DEFAULT NULL, `video_pubHour` int(10) DEFAULT NULL, `video_pubMinute` int(10) DEFAULT NULL, `video_pubSecond` int(10) DEFAULT NULL, `ownerMid` int(255) DEFAULT NULL, `ownerName` text CHARACTER SET utf8, `ownerFace` text CHARACTER SET utf8, `statView` int(255) DEFAULT NULL, `statLike` int(255) DEFAULT NULL, `statDanmaku` int(255) DEFAULT NULL, `statCoin` int(255) DEFAULT NULL, `statShare` int(255) DEFAULT NULL, `statFavorite` int(255) DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=915109 DEFAULT CHARSET=utf8mb4;"

cursor = db.cursor()  #获取cursor
cursor.execute('SET NAMES utf8mb4')  #设置字符集
cursor.execute("SET CHARACTER SET utf8mb4") #设置字符集
cursor.execute("SET character_set_connection=utf8mb4") #设置字符集
cursor.execute(create_table_videoContents_Sql); #如果不存在videoContents表自动创建


def log(contentStr = "",writeLog = False):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime(timeFormat, timeStruct)
    retStr = "[" + strTime + "] 输出内容:" + contentStr

    log_date = time.strftime("%Y-%m-%d", timeStruct)
    log_fn = log_dir + "/log_" + log_date + ".txt"

    if writeLog == True:
        with open(log_fn, "a",encoding='UTF-8') as file:
            file.write(retStr + "\n")

    print(retStr)


def getApiStr(apiUrl):
    global proxies
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001441) NetType/WIFI Language/zh_CN',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(apiUrl, headers=headers, data='',timeout=5,proxies=proxies)
        response.raise_for_status()

        if response.status_code == 200:
            resStr = response.text
        else:
            resStr = ""
            exit("[getApiStr] http状态码" + str(response.status_code)  +  " (未知错误)")
        return resStr
    except Exception as e:
        reprStr = str(repr(e))

        if "Precondition" in reprStr:
            restart_Second = sleepTime(0,15,0)
            exit("请求返回码412，已被反爬检测（建议关闭本机WiFi链接并重新连接后再次开启本程序），（同时）本程序将在15分钟后重启,详细内容:" + reprStr,restart_Second)
        else:
            restart_Second = sleepTime(0,0,10)
            exit("[getApiStr]请求出现异常（非被反爬检测），详细内容:" + reprStr + " 将在10秒后重启本程序",restart_Second)

def getLatestAid():
    with open(latestTxt, 'r', encoding='UTF-8') as f: # 打开文件
        lines = f.readlines() # 读取所有行
        first_line = lines[0] # 取第一行
        avInt = int(first_line)
        avInt = avInt + 1

        print("[getLatestAid]当前av号起点为:" +str(avInt))
    return avInt

def writeLatestAid(aidStr):
    try:
        with open(latestTxt, 'w',encoding='UTF-8') as f:
            f.write(str(aidStr))
            print("[writeLatestAid]写入最近处理的av号:" +aidStr)
    except Exception as e:
            reprStr = str(repr(e))
            restart_Second = sleepTime(0,0,10)
            exit("[writeLatestAid]写入最近记录时出席那问题（非被反爬检测），详细内容:" + reprStr + " 准备写入的av号: " + str(aidStr) + " 将在10秒后重启本程序 ",restart_Second)

def parseInsert(strJson):
    global db

    try:
        json.dumps(strJson,ensure_ascii=False)
        data = json.loads(strJson)
        code = str(data['code'])
    except Exception as e:
        reprStr = str(repr(e))
        restart_Second = sleepTime(0,0,10)
        exit("[parseInsert]解析json时失败,将在10秒后重启, 详细内容:" + reprStr + " 将在10秒后重启本程序",restart_Second)

    if code == "0":  #正确返回，处理如下
        data = data['data']

        if data.__contains__("cid") == False: #有些远古视频不包含cid这一项
            json_cid = 0
        else:
            json_cid = data['cid'] #cid

        #print(data)
        json_bvid = data['bvid'] #bv号
        json_aid = data['aid'] #aid

        json_tname = escape_string(data['tname']) #视频标签名
        json_pic = data['pic'] #视频封面url
        json_title = escape_string(data['title']) #视频标题
        json_desc = escape_string(data['desc'])  #视频简介

        json_pubdate = data['pubdate'] #视频发布时间戳
        pubYear = str(time.strftime('%Y', time.localtime(json_pubdate)))
        pubMonth = str(time.strftime('%m', time.localtime(json_pubdate)))
        pubDay = str(time.strftime("%d", time.localtime(json_pubdate)))
        pubHour = str(time.strftime('%H', time.localtime(json_pubdate)))
        pubMinute = str(time.strftime('%M', time.localtime(json_pubdate)))
        pubSecond = str(time.strftime('%S', time.localtime(json_pubdate)))

        json_owner = data['owner']
        json_ownerMid = str(json_owner['mid']) #mid就是用户id 拼接https://space.bilibili.com/ID号 得到
        json_ownerName = escape_string(str(json_owner['name'])) #up主名字
        json_ownerFace = str(json_owner['face']) #up主头像url

        json_stat = data['stat']
        json_statView = str(json_stat['view']) #浏览量
        json_statLike = str(json_stat['like'])  #点赞量
        json_statDanmaku = str(json_stat['danmaku']) #弹幕数量
        json_statShare = str(json_stat['share']) #分享数量
        json_statCoin = str(json_stat['coin']) #投币数量
        json_statFavorite = str(json_stat['favorite']) #收藏量

        sqlStr = """INSERT INTO `videoContents` (`aid`, `bvid`, `cid`, `video_title` , `video_desc` , `video_tname` , `video_pic`, `video_pubYear`, `video_pubMonth`, `video_pubDay`, `video_pubHour`, `video_pubMinute`, `video_pubSecond`, `ownerMid`, `ownerName`, `ownerFace`, `statView`, `statLike`, `statDanmaku` ,`statCoin` , `statShare` , `statFavorite`) VALUES ({},"{}",{},"{}","{}","{}","{}",{},{},{},{},{},{},{},"{}","{}",{},{},{},{},{},{});""".format(json_aid,json_bvid,json_cid,json_title,json_desc,json_tname,json_pic,pubYear,pubMonth,pubDay,pubHour,pubMinute,pubSecond,json_ownerMid,json_ownerName,json_ownerFace,json_statView,json_statLike,json_statDanmaku,json_statCoin,json_statShare,json_statFavorite)

        log("\n[parseInsert]准备执行的SQL语句如下:" + "\n" + sqlStr + "\n\n",False)
  
        try:
            conn = db.cursor()
            conn.execute(sqlStr)
            db.commit()
        except Exception as e:
            reprStr = str(repr(e))
            restart_Second = sleepTime(0,0,10)
            exit("[parseInsert]插入数据库时出现异常（非被反爬检测），详细内容:" + reprStr + " 待插入的MySQL语句: " + sqlStr + " 将在10秒后重启本程序 ",restart_Second)

        writeLatestAid(str(json_aid))  #记录已经插入数据库的最新aid

        log("[parseInsert]写入记录 aid:" + str(json_aid) + " 视频标题(作者):" + str(json_title) + "(" + str(json_ownerName) + ")",False)


    else:  #结果不存在，返回code不是0的情况如下
        log("[parseInsert]解析json失败,原因:" + data['message'] + " 当前aid:" + str(startAid),True)    

if __name__ == '__main__':
    bApi1 = "https://api.bilibili.com/x/web-interface/view?aid="  #视频信息api (aid自增，就是av号)
    
    time.sleep(2)  #启动前等待2秒，用于exit()调用本脚本自重启时防止潜在的id错位问题

    startAid = getLatestAid() #通过aid日志文件获取上一次退出时的aid +1（开始运行）

    while True:
        log("[main]当前aid" + str(startAid))
        a = getApiStr(bApi1 + str(startAid))
        parseInsert(a)
        startAid = int(startAid) + 1
        time.sleep(0.02)  #防反爬虫运行间隔，单位为秒