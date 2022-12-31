import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://filehelper.weixin.qq.com/") #打开微信网页版
driver.maximize_window()

def getApiContent(apiUrl):
    try:
        response = requests.get(apiUrl,timeout=8)
        response.raise_for_status()
        if response.status_code == 200:
            return response.text
    except Exception as e:
        reprStr = str(repr(e))
        print("[getApiStatus]请求Api时出错 (错误信息: {}）".format(reprStr))
        return "error"

def send(sendContentStr):   
    textEl = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div[3]/textarea")
    textEl.send_keys(sendContentStr)
    time.sleep(0.3)
    sendEl = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div[3]/div[2]/a")
    sendEl.click() #点击发送按钮
    print("[send]发送成功，内容为: {}".format(sendContentStr))

if __name__ == '__main__':
    print("[start]请在30秒内扫码登录")
    time.sleep(30)

    apiUrl1 = "http://127.0.0.1/bilibiliSpiderAdmin/getData.php?type=2"
    while True:
        send(getApiContent(apiUrl1))
        time.sleep(600) #等待多少秒后再次发送状态