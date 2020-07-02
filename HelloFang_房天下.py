import requests
#path-l 导包
from lxml import etree

def stripText(textList):
    '''
    将文本列表转化或字符串，并去掉其中包括的\n \t \r /-等字符
    :param textList: 文本列表
    :return: 字符串
    '''
    str_list=""
    for item in textList:
        item_str=item.replace('\n',"").replace('\r',"").replace('\t',"").replace('/',"").replace('-',"")
        #item_str=item.strip()当参数为空时，默认删除字符串两端的空白符（包括'\n','\r','\t','')
        if item_str!='':
            if str_list !='':
                str_list=str_list+","+item_str
            else:
                str_list=item_str
        return str_list

#U-A伪装
header={
"cookie":"new_search_uid=8bf1f40688a2aacf38351399dbfa6f6e; global_cookie=lglfd9l89hgioxkshyep96nna2qk7vliism; g_sourcepage=xf_lp%5Elb_pc; __utma=147393320.1262350275.1584431348.1584431348.1584431348.1; __utmc=147393320; __utmz=147393320.1584431348.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; xfAdvLunbo=; searchConN=1_1584431369_3368%5B%3A%7C%40%7C%3A%5D1e2db71e7adc2606bda589e87cdfbbac; city=cs; unique_cookie=U_lglfd9l89hgioxkshyep96nna2qk7vliism*8; __utmb=147393320.30.10.1584431348",
"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}
#第一步请求URL
#url="https://hengyang.newhouse.fang.com/house/s/"
base_url="https://cs.newhouse.fang.com/house/s/b9"

end_page=input("请输入要结束页：")
for p in range(1,int(end_page)+1):
    page=str(p)
    url=base_url+page+"/"
    param={
        'ctm':'1.hengyang.xf_search.page.'+page
    }

    #第二步：发出HTTP请求
    response=requests.get(url=url,headers=header)
    response.encoding="gbk"
    #第三步：获取响应的数据
    html_content=response.text
    #第四步：进行持久化
    # print(html_content)
    with open("fang"+page+".html",'w',encoding='gbk')as fp:
        fp.write(html_content)

    parse=etree.HTMLParser(encoding='gbk')
    tree=etree.parse("fang"+page+".html",parser=parse)
    # print(etree.tostring(tree,encoding='gbk').decode('gbk'))

    item_xpath="//div[@class='nhouse_list_content']/div[@class='nhouse_list']/div[@id='newhouse_loupai_list']/ul/li/div[@class='clearfix']"
    item_list=tree.xpath(item_xpath)
    # print(item_list)
    all_content=[]

    for item in item_list:
        if item.xpath("count(.//div[@class='nlc_details']/div[@class='house_value clearfix']/div[@class='nlcd_name']/a)")==0:
            continue
        item_dic={}

        name_xpath=".//div[@class='nlc_details']/div[@class='house_value clearfix']/div[@class='nlcd_name']/a/text()"
        name_list=item.xpath(name_xpath)
        item_dic['name']=stripText(name_list)
        # print(item_dic['name'])

        dist_xpath=".//div[@class='nlc_details']/div[@class='relative_message clearfix']/div/a/span/text()"
        dist_list = item.xpath(dist_xpath)
        item_dic['dist'] = stripText(dist_list)
        # print(item_dic['dist'])

        addr_xpath = ".//div[@class='nlc_details']/div[@class='relative_message clearfix']/div/a/text()[last()]"
        addr_list = item.xpath(addr_xpath)
        item_dic['addr'] = stripText(addr_list)
        # print(item_dic['addr'])

        price_xpath = ".//div[@class='nlc_details']/div[@class='nhouse_price']/span/text()"
        price_list = item.xpath(price_xpath)
        item_dic['price'] = stripText(price_list)
        # print(item_dic['price'])

        lebel_xpath = ".//div[@class='nlc_details']/div[contains(@class,'fangyuan')]/a/text()"
        lebel_list = item.xpath(lebel_xpath)
        item_dic['lebel'] = stripText(lebel_list)
        # print(item_dic['lebel'])

        room_xpath = ".//div[@class='nlc_details']/div[@class='house_type clearfix']/child::node()/text()"
        room_list = item.xpath(room_xpath)
        item_dic['room'] = stripText(room_list)
        # print(item_dic['room'])

        area_xpath = ".//div[@class='nlc_details']/div[@class='house_type clearfix']/text()"
        area_list = item.xpath(area_xpath)
        print(area_list)

        # item_dic['area'] = stripText(area_list)
        # print(item_dic['area'])

    #     all_content.append(item_dic)
    #
    # # 第四步：进行持久化
    # with open("fang"+page+".txt", 'w', encoding='UTF-8')as fp:
    #     for item in all_content:
    #         fp.write(str(item)+'\n')