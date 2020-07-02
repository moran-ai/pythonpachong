import requests
from bs4 import BeautifulSoup

url = 'https://www.liepin.com/zhaopin/'
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
}

key = input("请输入:")
end_page = input("请输入尾页:")
for page in range(1, int(end_page)+1):
    params = {
    'init':'-1',
    'headckid':'c96039a9ccc57cc2',
    'fromSearchBtn':'2',
    'ckid':'c96039a9ccc57cc2',
    'degradeFlag':'0',
    'sfrom':'click - pc_homepage - centre_searchbox - search_new',
    'key':key,
    'siTag':'_DX9xw1fxp0mmIOoIselPg~fA9rXquZc5IkJpXC - Ycixw',
    'd_sfrom':'search_fp',
    'd_ckId':'e8df7757031360bf27c91dc4c9b6acec',
    'd_curPage':'2',
    'd_pageSize':'40',
    'd_headId':'e8df7757031360bf27c91dc4c9b6acec',
    'curPage':page
    }
    response = requests.get(url, params=params, headers=headers)
    rep = response.text
    # 构建bs4对象
    soup = BeautifulSoup(rep, 'lxml')

    # 岗位名称
    title = soup.select('h3 a')

    # print(str(title))

    # 工资
    money = soup.select('span.text-warning')
    # print(str(money))

    # 招聘发布时间
    time = soup.select('p > time')
    # print(str(time))

    # 投递后反馈时间
    Response_time = soup.select('p > span:nth-child(2)')
    # print(str(Response_time))

    # 工作地址
    address = soup.select('p > a:nth-child(2)')
    # print(str(all))

    # 学历要求
    education_requirement = soup.select('p > span.edu')
    # print(str(education_requirement))

    # 工作经验
    work_experience = soup.select('p >span:nth-child(4)')
    # print(str(work_experience))

    # 公司名称
    company_name = soup.select('p.company-name > a')
    # print(str(company_name))

    # 存放内容
    content = []
    for i in range(len(address)):
        # 岗位名称
        ctitle = title[i].text
        ctitle.replace('  ', '').replace()
        print(str(ctitle))

        # 工资
        cmoney = money[i].text

        # 招聘发布时间
        ctime = time[i].text

        # 投递后反馈时间
        cResponse_time = Response_time[i].text

        # 工作地址
        caddress = address[i].text

        # 学历要求
        ceducation_requirement = education_requirement[i].text

        # 工作经验
        cwork_experience = work_experience[i].text

        # 公司名称
        ccompany_name = company_name[i].text

        # 构建数据
        data = {
            'title': ctitle,
            'money': cmoney,
            'time': ctime,
            'Response_time':cResponse_time,
            'address': caddress,
            'education_requirement': ceducation_requirement,
            'work_experience': cwork_experience,
            'company_name': ccompany_name
        }

        # print(data)
        # for s in data.keys():
        #     a = s.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
        content.append(data)
        # print(content)
        # for value in content:
        #     with open('猎聘.txt', 'a', encoding='utf-8') as f:
        #         # # read_data = f.read()
        #         # # read_data.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
        #         # for line in f:
        #         #     old_str = ('\n','\r', '\t')
        #         #     new_str = ' '
        #         #     if old_str in line:
        #         #         line = line.replace(old_str, new_str)
        #         #     file_data += line
        #         f.write(str(value)+'\n')
        #         file = open('猎聘网.txt', 'w')
        #         for k, v in data.items():
        #             file.write(str(k)+' '+str(v) + '\n')
        #         file.close()

