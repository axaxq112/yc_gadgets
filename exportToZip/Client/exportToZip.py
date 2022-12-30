import sys
import argparse
import shutil
import os
import time
import yaml
import smtplib
import requests
from openpyxl import load_workbook
from email.mime.text import MIMEText
from email.header import Header

parser = argparse.ArgumentParser()
parser.add_argument('-v','--ver',help="需要打包的程序版本号",required=True)
parser.add_argument('-s','--send',help="发送打包文件至指定邮箱（不传则不发送）")
args = parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    ver = args.ver
    send = args.send

    if send == None:
        print("即将开始导出 版本[{0}] 本地打包不发送 \n".format(ver))
    else:
        print("即将开始导出 版本[{0}] 发送至[{1}] \n".format(ver,send))

    programDir = os.getcwd()
    workDir = os.path.abspath("../../") #需要打包的文件的目录
    workDir2 = workDir + "/" + ver

    if not os.path.exists(workDir2):
        print("导出失败 {0}目录不存在".format(workDir2))
        sys.exit(1)
    
    outputZipDir = workDir + "/output" + ver
    if not os.path.exists(outputZipDir):
        os.mkdir(outputZipDir)

    timeStr = time.strftime(r"%Y%m%d%H%M%S")
    outputFileName = "/{0}_ver{1}".format(timeStr,ver)
    outputZipPath = outputZipDir + outputFileName
    try:
        a = shutil.make_archive(outputZipPath,"zip",workDir2)
    except Exception as err:
        reprStr = repr(err)

    if a:
        print("导出成功: {0}".format(outputZipPath))
    else:
        print("导出失败，原因:{0}".format(reprStr))
        sys.exit(1)

    if send != None:
        with open("exportToZipConfig.yaml",encoding="UTF-8") as fr:
            config = yaml.safe_load(fr)

        if config["smtpServer"] != None and config["smtpPort"] != None and config["smtpUser"] != None and config["smtpCode"] != None and config["innerApi"] != None and config["apiReqPass"]:
            smtpServer = config["smtpServer"]
            smtpPort = config["smtpPort"]
            smtpUser = config["smtpUser"]
            smtpCode = config["smtpCode"]

            innerApi = config["innerApi"]
            apiReqPass = config["apiReqPass"]

            getInnerLink = innerApi + "?type=inner&reqPass={0}&ver={1}&absPath={2}.zip".format(apiReqPass,ver,outputZipPath)
            getOuterLink = innerApi + "?type=outer&reqPass={0}&ver={1}&absPath={2}.zip".format(apiReqPass,ver,outputZipPath)

            print(getInnerLink);

            try:
                getInnerLinkReq = requests.get(getInnerLink)
                getOuterLinkReq = requests.get(getOuterLink)
            except Exception as err:
                errStr = reprStr(err)
                print("\n 请求分享链接接口失败，原因:{0} 发送失败".format(errStr))
                sys.exit(1)

            innerLink = getInnerLinkReq.text
            outerLink = getOuterLinkReq.text

            if len(innerLink) <= 15 and len(outerLink) <= 15 or innerLink == None or outerLink == None:
                print("\n分享链接接口返回值过小，发送失败")
                sys.exit(1)
            elif getOuterLinkReq.status_code == 404 or getInnerLinkReq.status_code == 404:
                print("\n分享链接接口链接有误【404】，发送失败")
                sys.exit(1)
            elif getOuterLinkReq.status_code == 502 or getInnerLinkReq.status_code == 502:
                print("\n分享链接接口服务器返回有误【502】，发送失败")
                sys.exit(1)
            elif getOuterLinkReq.status_code != 200 or getInnerLinkReq.status_code != 200:
                print("\n分享链接接口服务器返回有误【{0}|{1}】，发送失败".format(getInnerLinkReq.status_code,getOuterLinkReq.status_code))
                sys.exit(1)

            print("\n 解析配置文件成功，已获取2个分享链接，即将使用SMTP发送邮件")

            smtp_obj = smtplib.SMTP_SSL(smtpServer, smtpPort)
            smtp_obj.login(smtpUser, smtpCode)
            msg_context = """<h3>导出时间: {0}<h3>
                            <h3>导出版本: {1}</h3>
                            <br>内网下载地址(有效期30日): {2}
                            <br>外网下载地址（有效期3日）: {3}
                            """.format(timeStr,ver,innerLink,outerLink)

            msg = MIMEText(msg_context, 'html', 'GBK')
            msg['from'] = Header('导出自动发件', 'GBK')
            msg['Subject'] = Header('导出', 'GBK')

            errStr = ""
            try:
                sendObj = smtp_obj.sendmail(smtpUser,send,msg.as_string()) #send为收件人地址
            except Exception as err:
                errStr = reprStr(err)

            if errStr == "":
                print("\n 发送成功，请:{0} 自行查看".format(send))
            else:
                print("\n 发送失败，原因:{0}".format(errStr))