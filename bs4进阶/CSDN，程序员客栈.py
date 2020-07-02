import requests
#导入bs4库文件
from bs4 import BeautifulSoup

def request(url,url_list,header,word,page):
    if url_list==1:
        # parm参数
        param = {
            "q": word,
            "p": page
        }
        response = requests.get(url, headers=header, params=param)
        # 3：获得网站响应数据
        html = response.text
        return html
    elif url_list==2:
        param = {
            "keyword": word,
            "page": str(page)
        }
        response = requests.get(url, headers=header, params=param)
        # 3：获得网站响应数据
        html = response.text
        return html

def tree_data(html,list):

    if list == 1:
        # 构建bs4对象
        soup = BeautifulSoup(html, 'lxml')
        # 标题
        name = soup.select('div.limit_width > a:nth-child(2)')
        # print(str(name))
        # 作者
        father = soup.select('div.search-list-con dd.author-time')
        # print(str(father))
        content = []
        for i in range(len(name)):
            # 用户名
            cName = name[i].text
            # print(cName)
            cAddress = father[i].text
            # print(cAddress)
            # 构建数据
            c = {
                'name': cName.strip(),
                'address': cAddress.strip()
            }
            content.append(c)
        print(content)
        return content

    elif list == 2:
        soup = BeautifulSoup(html, 'lxml')
        # 用户名标签列表<p class="user-name" style="">python大拿</p>
        name = soup.select('p.user-name')
        # print(str(name))
        # 职位标签列表<div class="title"><a href="https://www.proginn.com/wo/202972" target="_blank" class="info" userid="202972" title="中国电信python高级开发工程师">
        title = soup.select('div.title a.info')  # ('div.title > a,info')   一定要有空格
        # print(str(title))
        # 技能 父节点中的第二个子节点中的span标签
        skill = soup.select('p.desc-item:nth-child(2) > span')  # :nth-child(2)=第二个p标签中的span标签
        # print(str(skill))
        # 作品
        work = soup.select('p.desc-item:nth-child(3) > span')  # :nth-child(3)=第二个p标签中的span标签
        # 工作地点和时间  父节点列表
        father = soup.select('div.work-time')
        # print(str(father))
        # 存放内容  因为以上都是列表的形式
        content = []
        for i in range(len(name)):
            # 用户名
            cName = name[i].text
            # 职位
            cTitle = title[i].text
            # 技能
            cSkills = skill[i].text
            # 作品
            cWorks = work[i].text
            # 工作地点
            cAddress = father[i].div.text
            # 工作时间
            for t in father[i].div.next_siblings:
                cTime = t.text
            # 构建数据
            c = {
                'name': cName,
                'position': cTitle.strip(),
                'skills': cSkills.strip(),
                'works': cWorks.strip(),
                'address': cAddress.strip()
            }
            content.append(c)
        print(content)
        return content

def baocun(data):
    for value in data:
        with open('jihe.txt', 'a', encoding='utf-8') as file:
            file.write(str(value) + '\n')

if __name__ == "__main__":
    # 用户输入
    url_list = int(input("搜索网站[1:CSDN 2:程序员客栈 3:退出]:"))
    word = input("请输入搜索关键字：（退出：3）")#Python工程师
    end_page = input("请输入结束页：（退出：3）")
    while url_list!=3 and end_page!=3:
        # 伪请求头
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"
        }

        for page in range(1, int(end_page) + 1):
            url = ['https://so.csdn.net/so/search/s.do',
                   'https://www.proginn.com/search']
            html = request(url[url_list - 1],url_list,header,word,page)
            data = tree_data(html, url_list)
            baocun(data)

        url_list = int(input("搜索网站[1:CSDN 2:程序员客栈 3:退出]:"))
        word = input("请输入搜索关键字：（退出：3）")#Python工程师
        end_page = input("请输入结束页：（退出：3）")
