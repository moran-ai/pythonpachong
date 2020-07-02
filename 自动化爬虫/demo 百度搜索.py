# encoding:gbk
from selenium import webdriver
import time

# 创建浏览器对象
browser = webdriver.Chrome()

# 发送请求
browser.get('https://www.baidu.com/')

# 定位到搜索框
ele = browser.find_element_by_xpath('//*[@id="kw"]')

# 搜索框中写入文字
ele.send_keys('python')

# 停止等待
time.sleep(2)

# 定位到百度一下按钮
browser.find_element_by_xpath('//*[@id="su"]').click()

# 停止等待
time.sleep(5)

# 截图
browser.save_screenshot('baidu.png')

# 关闭
browser.quit()
