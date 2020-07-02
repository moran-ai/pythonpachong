import requests
from bs4 import BeautifulSoup

def get_http(url, headers, params):
    response = requests.get(url, params=params, headers=headers)
    rep = response.text
    return rep

def analysis(soup):
    # 标题
    title = soup.select('a.title')
    # print(str(title))

    # up主
    author = soup.select('span.so-icon:nth-child(4) > a')
    # print(str(author))

    # 观看次数
    watch_num = soup.select('div.tags > span:nth-child(1)')
    # print(str(watch_num))

    # 上传时间
    time = soup.select('div.tags > span:nth-child(3)')
    # print(str(time))

    # 弹幕
    barrage = soup.select('div.tags > span:nth-child(2)')
    # print(str(barrage))

    # 存放内容
    content = []
    for i in range(len(author)):
        # 标题
        ctitle = title[i].text

        # up主
        cauthor = author[i].text

        # 观看次数
        cwatch_num = watch_num[i].text

        # 上传时间
        ctime = time[i].text

        # 弹幕
        cbarrage = barrage[i].text

        data = {
            '标题': ctitle,
            'up主': cauthor,
            '观看次数': cwatch_num,
            '上传时间': ctime,
            '弹幕': cbarrage
        }
        content.append(data)
        return content

def save(content):
    # 存储到本地
    for value in content:
        with open('bilibli.txt', 'a', encoding='utf-8') as f:
            f.write(str(value)+'\n')

def main():
    url = 'https://search.bilibili.com/all'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
    }
    keyword = input("请输入:")
    end_page = input("请输入结尾页面:")
    for page in range(1, int(end_page)+1):
        params = {
            'keyword': keyword,
            'page': page
        }
        rep = get_http(url, headers,params)
        # 构建bs4对象
        soup = BeautifulSoup(rep, 'lxml')
        content = analysis(soup)
        save(content)
main()
