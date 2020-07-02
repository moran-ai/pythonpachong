# encoding:gbk
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
print(driver.page_source)
driver.close()
# sleep(2)
#
# driver.quit()
