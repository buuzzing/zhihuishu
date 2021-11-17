# coding=utf-8

from selenium import webdriver
from datetime import datetime
from time import sleep as manualWait
import json
import io, sys
import re

# ------------ 修改以下三个参数以符合实际需求 ------------ #

# 整数，单次运行回答的题目数
# 可根据需要自行修改
TOTNUMBER = 5

# 修改为你的日志路径，用于记录每次讨论的详细信息
# 必须修改，例子: pathToLog = r'/home/user/log.txt'
pathToLog = PATH_TO_YOUR_LOG

# 修改为你的 Cookies 路径，用于记录你的登录信息
# 必须修改，例子: pathToCookies = r'/home/user/cookies.txt'
pathToCookies = PATH_TO_YOUR_COOKIES

# ------------ 以下内容不应被修改 ------------ #

url0 = r'https://passport.zhihuishu.com/login'
url1 = r'https://onlineweb.zhihuishu.com'

pathToList = r'#app > div > div.web-qa-body > div.web-qa-main-left > div > ' \
             r'div.infinite-list-wrapper.question-list-container.el-scrollbar > div.el-scrollbar__wrap > div > ul > ' \
             r'li:nth-child('  # 151)
pathToQuestion = r'//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[1]/div/ul/li['  # 189]/div[2]
pathToAnswerNum = r'//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[1]/div/ul/li['  # 189]/div[3]/div[1]/div[1]

pathToKey = r'//*[@id="app"]/div/div[3]/div[1]/div[2]/ul/li[2]/div[3]/p/span'
pathToAnswer = r'//*[@id="app"]/div/div[4]'
pathToTextarea = r'//*[@id="app"]/div/div[5]/div/div/div[2]/div/div[1]/div/textarea'
pathToSubmit = r'//*[@id="app"]/div/div[5]/div/div/div[2]/div/div[2]/div'
pathToMyAnswer = r'//*[@id="app"]/div/div[3]/div[1]/div[2]/ul/li[1]/div[3]/div[2]/div[1]/i'


class GoToSleep:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def changePage(self, url) -> None:  # 切换页面，隐式等待 30 秒
        self.driver.get(url)
        self.driver.implicitly_wait(30)

    def login(self) -> None:  # 利用 Cookies 登录
        self.changePage(url0)
        self.driver.delete_all_cookies()
        with open(pathToCookies, 'r') as f:
            cookies_list = json.load(f)
            for cookie in cookies_list:
                # expiry 字段出错，改为 int 型后不报错
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
        self.driver.refresh()
        manualWait(3.5)

    def changeToCourse(self) -> None:  # 切换至问答页面的“最新”选项卡
        self.changePage(url1)
        manualWait(5)
        qa = self.driver.find_element_by_xpath(r'//*[@id="sharingClassed"]/div[2]/ul/div/dl/dt/div[2]/ul/li[3]/a')
        url_tmp = qa.get_attribute('href')
        self.changePage(url_tmp)
        manualWait(3)
        qn = self.driver.find_element_by_xpath(r'//*[@id="app"]/div/div[2]/div[1]/div/div[1]/div[2]')
        qn.click()
        manualWait(3)

    def scrollDown(self) -> None:  # 向下滚动 50 条回答
        js = r'document.querySelector("' + pathToList + str(50) + r')").scrollIntoView(true)'
        self.driver.execute_script(js)
        self.driver.implicitly_wait(30)
        manualWait(3.7)

    def work(self) -> int:  # 选择 TOTNUMBER 条问题
        tot, base = 0, 41
        while tot < TOTNUMBER:
            js = r'document.querySelector("' + pathToList + str(base) + r')").scrollIntoView(true)'
            self.driver.execute_script(js)
            self.driver.implicitly_wait(30)
            pos0 = pathToQuestion + str(base) + r']/div[2]'
            pos1 = pathToAnswerNum + str(base) + r']/div[3]/div[1]/div[1]'
            base += 1
            qa = self.driver.find_element_by_xpath(pos0)  # 问题
            qn = self.driver.find_element_by_xpath(pos1)  # 回答数
            num = qn.text
            num = re.sub(r'\D', '', num)
            if int(num) > 10:
                write_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S') + '\n'
                question_content = 'Question:\t' + qa.get_attribute('title') + '\n'
                question_number = 'Number:\t\t' + num + ' 个回答' + '\n'
                tot += 1
                qa.click()
                windows = self.driver.window_handles
                self.driver.switch_to.window(windows[1])
                key = self.driver.find_element_by_xpath(pathToKey)
                my_answer = 'My Answer:\t' + key.text + '\n\n'
                manualWait(2.9)
                try:
                    self.driver.find_element_by_xpath(pathToAnswer).click()
                    manualWait(2.3)
                    self.driver.find_element_by_xpath(pathToTextarea).click()
                    self.driver.find_element_by_xpath(pathToTextarea).send_keys(key.text)
                    manualWait(5.1)
                    self.driver.find_element_by_xpath(pathToSubmit).click()
                    manualWait(1)
                    with open(pathToLog, 'a') as f:
                        f.write(write_time)
                        f.write(question_content)
                        f.write(question_number)
                        f.write(my_answer)
                    self.driver.refresh()
                    manualWait(1)
                    self.driver.find_element_by_xpath(pathToMyAnswer).click()
                except BaseException:
                    pass
                manualWait(1.3)
                self.driver.close()
                self.driver.switch_to.window(windows[0])
                manualWait(1)
        return tot

    def zzz(self) -> None:  # 任务完成，去睡觉
        self.driver.close()


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    haveSleep = GoToSleep()
    haveSleep.login()
    haveSleep.changeToCourse()
    haveSleep.scrollDown()
    haveSleep.work()
    haveSleep.zzz()
