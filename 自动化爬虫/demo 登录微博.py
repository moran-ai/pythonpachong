# encoding:gbk
from selenium import webdriver
import time

# 创建浏览器对象
broswer = webdriver.Chrome()

# 发送请求,打开微博首页
broswer.get('https://weibo.com/')

time.sleep(5)
# 用户名
broswer.find_element_by_css_selector('#loginname').send_keys('18974498571')

# 密码
broswer.find_element_by_css_selector('.info_list.password input[node-type="password"]').send_keys('cai201314')

# 点击登录
broswer.find_element_by_css_selector('.info_list.login_btn a[node-type="submitBtn"]').click()

# 登陆后获取用户名
time.sleep(10)
name = broswer.find_element_by_css_selector('.nameBox a').text
print(f'用户名为：{name}')

time.sleep(1)
# 关闭浏览器
broswer.quit()
