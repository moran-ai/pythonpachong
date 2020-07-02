import requests
from bs4 import BeautifulSoup

# 发送请求
def get_http(url, headers,params):
    response = requests.get(url, params=params, headers=headers)
    rep = response.text
    return rep

# 数据解析
def analysis(soup):
    # 标题
    title = soup.select('div.limit_width > a ')
    # print(str(title))
    # 作者
    author = soup.select('dd.author-time:nth-child(2) > a')
    # print(str(author))
    # 浏览量
    view = soup.select('dd.author-time:nth-child(3) > span.mr16')
    # print(str(view))
    # 发布时间
    time = soup.select('dd.author-time:nth-child(3) > span.date')
    # print(str(time))

    # 存放内容
    content = []
    for i in range(len(author)):
        # 标题
        ctitle = title[i].text
        # 作者
        cauthor = author[i].text
        # 浏览量
        cview = view[i].text
        # 发布时间
        ctime = time[i].text

        # 构建数据
        c = {
            'name': ctitle,
            'author': cauthor,
            'view': cview,
            'time': ctime
        }
        content.append(c)
        return content

# 保存文件到本地
def save(content):
    for value in content:
        with open('cd.txt', 'a', encoding='utf-8') as f:
            f.write(str(value)+'\n')

# 运行
def main():
    url = 'https://so.csdn.net/so/search/s.do'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
    }
    q = input("请输入关键字:")
    end_p = input("请输入结束页面：")
    for p in range(1, int(end_p) + 1):
        params = {
            'q': q,
            'p': p
        }
        rep = get_http(url, headers,params)
        soup = BeautifulSoup(rep, 'lxml')
        data = analysis(soup)
        save(data)
main()

