# encoding:gbk
from selenium import webdriver
import time

# �������������
broswer = webdriver.Chrome()

# ��������,��΢����ҳ
broswer.get('https://weibo.com/')

time.sleep(5)
# �û���
broswer.find_element_by_css_selector('#loginname').send_keys('18974498571')

# ����
broswer.find_element_by_css_selector('.info_list.password input[node-type="password"]').send_keys('cai201314')

# �����¼
broswer.find_element_by_css_selector('.info_list.login_btn a[node-type="submitBtn"]').click()

# ��½���ȡ�û���
time.sleep(10)
name = broswer.find_element_by_css_selector('.nameBox a').text
print(f'�û���Ϊ��{name}')

time.sleep(1)
# �ر������
broswer.quit()
