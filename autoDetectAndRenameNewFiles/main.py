####本程序推荐使用sudo后执行
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

dir_path = "/Users/susie/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/4dabd161d78fb6875f008776aa91b9c1/Message/MessageTemp" #到MessageTemp目录即可
log_dir = "detectLogs"

def checkTxtExistOrCreate(txtPath):
    file = txtPath
    if os.path.exists(file):
        sz = os.path.getsize(file)
        if not sz:
            file = open(txtPath,'w')
            file.write('|')
            file.close()
            print("[checkTxtExistOrCreate] '{}' 文件为空，已写入默认内容".format(txtPath))
        else:
            print("[checkTxtExistOrCreate] '{}' 文件大小为: {}B".format(txtPath,str(sz)))
    else:
        print("[checkTxtExistOrCreate]本程序文件同级目录中不存在 '{}'文件，将自动创建".format(txtPath))
        file = open(txtPath,'w')
        file.write('|')
        file.close()

def log(contentStr = "",showLog = True):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    timeFormat = '%Y-%m-%d %H:%M:%S'
    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime(timeFormat, timeStruct)
    retStr = "[" + strTime + "] 输出:" + contentStr
    log_date = time.strftime("%Y-%m-%d", timeStruct)
    log_fn = log_dir + "/detectLog_" + log_date + ".txt"
    checkTxtExistOrCreate(log_fn)
    
    with open(log_fn, "a",encoding='UTF-8') as file:
       file.write(retStr + "\n")

    if showLog == True:
        print(retStr)

def getTimeStr():
    strTime = str(time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time()))))
    return strTime

class CreateEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        srcPath = event.src_path
        dstPath = event.dest_path
        dstFileDir = os.path.dirname(dstPath) #微信移动目标目录路径
        dstFileName = os.path.basename(dstPath) #微信移动目标文件名

        if event.is_directory == False and "File/" in dstPath and "bak" not in srcPath and ".DS_Store" not in srcPath:
            log("[on_moved]检测到微信文件完成下载: 原路径: {}  目标路径: {}".format(srcPath,dstPath))

            ourFileName = dstFileName + "." + getTimeStr() + "." + "bak"
            ourFilePath = os.path.join(dstFileDir, ourFileName)

            try:
                os.rename(dstPath,ourFilePath)
            except Exception as e:
                reprStr = str(repr(e))
                log("[on_moved]在重命名微信下载文件时出现错误：原因: {}".format(reprStr))
            else:
                log("[on_moved]重命名微信下载文件成功,原路径: {} 已重命名为: {}".format(dstPath,ourFilePath))

        elif event.is_directory == False and "/OpenData" in dstFileDir:  #自己人上传文件（忽略）
            log("[on_moved]检测到自己人上传文件（忽略） {}".format(dstPath),True)

        elif event.is_directory == False and ".bak" in dstPath: #自己人的重命名操作（忽略）
            log("[on_moved]检测到自己人重命名(忽略) {}".format(dstPath),False)
        else:
            log("file moved from {0} to {1}".format(event.src_path, event.dest_path))

        if event.is_directory:
            log("[on_moved]检测到文件夹移动： 原路径: {} 目标路径: {}".format(srcPath, dstPath))

    # def on_deleted(self, event):
    #     if event.is_directory:
    #         log("[on_deleted]文件夹被删除(路径: {})".format(event.src_path))
    #     else:
    #         log("[on_deleted]文件被删除: 路径: {}".format(event.src_path))

    def on_created(self, event):
        if event.is_directory:
            newDirPath = event.src_path
            log("[on_created]目录创建:{}".format(newDirPath))
        elif event.is_directory == False and "/OpenData" in event.src_path: #自己人上传文件（忽略）
            log("[on_moved]检测到自己人上传文件（忽略） {}".format(event.src_path))

        else: #走到这里后，下面就重命名文件
            ignoreStatus = False #默认不忽略文件
            newFileSrcPath = event.src_path
            newFileDir = os.path.dirname(newFileSrcPath) #输出新文件所属目录
            newFileName = os.path.basename(newFileSrcPath) #输出新文件文件名
            newFileSuffix =  os.path.splitext(newFileSrcPath)[-1] #输出新文件后缀内容
            newFileSuffix = newFileSuffix.lower()

            #—————— Start 忽略的类型 ——————————————
            if newFileSrcPath.endswith(".DS_Store"):
                ignoreStatus = True
            elif newFileSrcPath.endswith(".aud.silk"):
                ignoreStatus = True #忽略语音类型的文件（可以正常听语音、转文字）
            elif newFileSrcPath.endswith(".pic_thumb.jpg"):
                ignoreStatus = False #不忽略缩略图
            elif newFileSrcPath.endswith(".pic_thumb.png"):
                ignoreStatus = False #不忽略缩略图
            elif newFileSrcPath.endswith(".dftemp.jpg"):
                ignoreStatus = True
            elif newFileSrcPath.endswith(".dftemp.png"):
                ignoreStatus = True
            elif newFileSuffix == ".dftemp":
                ignoreStatus = True
            #————————忽略类型 End ——————————————

            if  ignoreStatus == False:
                dstFileName = newFileName + "." + getTimeStr() + "." + "bak"
                dstFilePath = os.path.join(newFileDir, dstFileName)

                #log("[on_created]记录:{} 新文件名:{} 所属路径: {} 后缀:{}".format(newFileSrcPath,dstFileName,newFileDir,newFileSuffix))
                
                try:
                    os.rename(newFileSrcPath,dstFilePath) #重命名文件

                except Exception as e:
                    reprStr = str(repr(e))
                    log("[on_created]在重命名文件时出现错误：详细原因: {}".format(reprStr))
                else:
                    if "thumb" in newFileName:
                        log("[on_created]重命名文件成功,已将缩略图: {} 重命名为:{}".format(newFileName,dstFilePath))
                    elif ".pic.jpg" or ".pic.png" in newFileName:
                        log("[on_created]重命名文件成功,已将原图: {} 重命名为:{}".format(newFileName,dstFilePath))
                    else:
                        log("[on_created]重命名文件成功,已将: {} 重命名为:{} (所属目录:{})".format(newFileName,dstFileName,newFileDir))

            else:
                log("[on_created]忽略文件新建: 文件路径:{}".format(newFileSrcPath))

if __name__ == '__main__':
    log("[main]准备开始检测")
    observer = Observer()
    event_handler = CreateEventHandler()
    observer.schedule(event_handler,dir_path,True)
    observer.start()
    try:
        while True:
            time.sleep(0.01)
    finally:
        observer.stop()
        observer.join()