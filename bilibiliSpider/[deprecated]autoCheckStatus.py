#本文件用于保证main.py 24小时执行（崩溃自重启）
import time
import os
import subprocess

def sleepTime(hour, min, sec):
    return hour * 3600 + min * 60 + sec

def log(contentStr = ""):
    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)
    retStr = "[" + strTime + "] 输出内容:" + contentStr

    log_date = time.strftime("%Y-%m-%d", timeStruct)
    log_fn = "checkStatus_" + log_date + ".txt"
    with open(log_fn, "a",encoding='UTF-8') as file:
        file.write(retStr + "\n")
    print(retStr)

def readTxt():
    aidStr = ''
    with open("latestAid.txt", 'r', encoding='utf-8') as f:
        rows = f.readlines()
        if len(rows) == 0:
            log("[readText]目标文件无内容")
            aidStr = "error"
        else:
            aidStr = str(rows[0])
    return aidStr

def getLatestAid():
    aidStr = ''
    retryCount = 0
    retryTime = 20

    for x in range(0, retryTime):
        retStr = ""
        aidStr = readTxt()
        if aidStr != "error":
            log("[getLatestAid] aid:" + aidStr)
            retStr = aidStr
            break
        else:
            log("[getLatestAid]准备重新读取Txt,重试第"+ str(retryCount) +"次" )
            retryCount = retryCount + 1
            retStr = "error"
            time.sleep(0.5)
    return retStr

def checkStatus():
    global aidTemp
    log("开始检测同级目录中latestAid.txt是否有变动")
    aidNow = getLatestAid()
    if aidTemp == aidNow: #在间隔内无变动-》main.py挂了，调用重开
        captureFn = str(time.time())
        os.system("screencapture " + captureFn + ".png")
        log("检测对象可能发生崩溃，即将重开,重开前已截图[" + captureFn + ".png]")
        subprocess.Popen(f'open startMain.command', shell=True)
    elif aidNow == "error":
        log("[checkStatus]读取Txt时出错，准备下一次检测")
    else:
        newNum = int(aidNow) - int(aidTemp)
        log("正常运行: " + str(checkInterval) +"秒前结果为: " + str(aidTemp) +",当前结果: " + str(aidNow) + ",新增数据:" + str(newNum) + "条")
        aidTemp = getLatestAid()
        if aidTemp == "error":
            aidTemp = getLatestAid()
            if aidTemp == "error":
                exit("已重试两次，aid均为空，程序将退出")

aidTemp = getLatestAid()  #保存旧的aid，与新的进行判断
if aidTemp == "error":
    exit("初始化时出现错误，latestAid.txt不能为空")

checkInterval = sleepTime(0,0,35) #检测main.py运行状态间隔（不宜过大）

log("Start autoCheck Interval:" + str(checkInterval))
while True:
    time.sleep(checkInterval)
    checkStatus()