from selenium import webdriver
import time

url0 = r'https://passport.zhihuishu.com/login'
url1 = r'https://onlineweb.zhihuishu.com'
username = r'username'
password = r'password'

def login(browser):
    browser.get(url0)
    browser.implicitly_wait(10)
    time.sleep(2)
    browser.find_element_by_id('lUsername').send_keys(username) # 用户名
    time.sleep(2)
    browser.find_element_by_id('lPassword').send_keys(password) # 密码
    time.sleep(2)
    rem = browser.find_element_by_xpath('//input[@name="remember"]')    # 记住我
    if not rem.is_selected():
        rem.click()
    time.sleep(2)
    browser.find_element_by_id('f_sign_up').submit()    # 登录
    browser.implicitly_wait(10)
    
def changeToCourse(browser):
    browser.get(url1)
    browser.implicitly_wait(10)
    time.sleep(10)
    qa = browser.find_element_by_xpath('//*[@id="sharingClassed"]/div[2]/ul/div/dl/dt/div[2]/ul/li[3]/a')
    url_tmp = qa.get_attribute('href')
    browser.get(url_tmp)
    browser.implicitly_wait(10)

if __name__ == '__main__':
    browser = webdriver.Chrome()
    login(browser)
    time.sleep(5)
    changeToCourse(browser)
    time.sleep(5)
    browser.quit()
