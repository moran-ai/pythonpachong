# encoding:gbk
from selenium import webdriver
import time

# �������������
browser = webdriver.Chrome()

# ��������
browser.get('https://www.baidu.com/')

# ��λ��������
ele = browser.find_element_by_xpath('//*[@id="kw"]')

# ��������д������
ele.send_keys('python')

# ֹͣ�ȴ�
time.sleep(2)

# ��λ���ٶ�һ�°�ť
browser.find_element_by_xpath('//*[@id="su"]').click()

# ֹͣ�ȴ�
time.sleep(5)

# ��ͼ
browser.save_screenshot('baidu.png')

# �ر�
browser.quit()
