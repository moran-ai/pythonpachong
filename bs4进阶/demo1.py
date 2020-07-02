import requests
from bs4 import BeautifulSoup

url = 'https://www.proginn.com/search'
headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
}

# 以循环的形式发送http请求
keyword = input("请输入关键字:")
end_p = input("请输入结束页面:")
for page in range(1, int(end_p)):
    # param参数
    params = {
        'keyword': keyword ,
        'page': page
    }
    # 发送请求
    response = requests.get(url, params=params, headers=headers)
    rep = response.text
    filename = str(page)+'.html'
    # with open(filename, 'w', encoding='utf-8') as f:
    #     f.write(rep)
    # 构建bs4对象
    # 用户名标签列表
    soup = BeautifulSoup(rep, 'lxml')
    name = soup.select('p.user-name')
    # print(name)
    # 职位标签名
    title = soup.select('div.title > a.info')
    # print(str(title))

    # 技能,选择属于其父元素的第二个子元素的span标签
    skill = soup.select('p.desc-item:nth-child(2) > span')
    # print(skill)

    # 作品
    work = soup.select('p.desc-item:nth-child(3) > span')
    # print(work)

    # 工作地点和时间
    father = soup.select('div.work-time')
    # print(str(father))
    # 存放内容
    content = []
    for i in range(len(name)):
        # 用户名
        cName = name[i].text
        # 职位
        ctitle = title[i].attrs['title']
        # 技能
        cskill = skill[i].text
        # 作品
        cwork = work[i].text
        # 工作地点
        cfather = father[i].div.text
        # 工作时间  next_siblings 兄弟节点
        for t in father[i].div.next_siblings:
            cTime = t.text
        # print(str(type(father[i].div.next_siblings)))

        # 构建数据
        c = {
            'name':cName,
            'title':ctitle,
            'skill':cskill,
            'work':cwork,
            'address':cfather,
            'time':cTime
        }
        content.append(c)
    for value in content:
        with open('progame.txt', 'a', encoding='utf-8') as f:
            f.write(str(value)+'\n')

