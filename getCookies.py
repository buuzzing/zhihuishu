import json
import time

from selenium import webdriver

# ------------ 修改以下两个参数以符合实际需求 ------------ #

# 整数，为登录时的等待时间
# 你需要在 waitTime 秒内完成登录
# 接下来等着浏览器自动关闭就可以了
# （如果你手速较慢，可以把它改的大一些
waitTime = 20

# 修改为你的 Cookies 路径，用于记录你的登录信息
# 必须修改，例子: pathToCookies = r'/home/user/cookies.txt'
# 注意：这个路径需要和 work.py 下的 Cookies 路径保持一致
pathToCookies = PATH_TO_YOUR_COOKIES

# ------------ 以下内容不应被修改 ------------ #

driver = webdriver.Chrome()

driver.get('https://passport.zhihuishu.com/login')

time.sleep(waitTime)

with open(pathToCookies, 'w') as f:
    f.write(json.dumps(driver.get_cookies()))

driver.close()
