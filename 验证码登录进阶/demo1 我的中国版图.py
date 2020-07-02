# encoding:gbk
import requests
from fake_useragent import UserAgent
from YDMHTTPUbil import YDMHttp

def checkValidCode(fileName, codeType):
    # 用户名
    username = 'qz_cai'

    # 密码
    password = 'cai_201314'

    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appid = 10525

    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appkey = '30c380d8645c5b722dbcdc979efa4f8a'

    # 图片文件
    filename = fileName

    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype = codeType

    # 超时时间，秒
    timeout = 60

    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login();
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance();
        print('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout);
        print('cid: %s, result: %s' % (cid, result))
        return result

headers = {
    'User-Agent': str(UserAgent().random)
}
session = requests.Session()

# 获得验证码
img_url = 'http://211.159.149.56/sbsm/supermap/codeImg.do'
img_response = session.get(img_url, headers=headers)
img_response.encoding = img_response.apparent_encoding
img_rep = img_response.content
# print(img_response.status_code)

# 保存验证码
with open('code.jpg', 'wb') as f:
    f.write(img_rep)

code = checkValidCode('code.jpg', 1004)
print(code)

# # img_code = input("请输入验证码: ")
# data = {
# 'userName': '18974498571',
# 'enPassWord': '387f5d2b9b0f6bb0dc17cc1f768e9937',
# 'passWord': 'CAI201314++',
# 'validataCade': code
# }
#
# url = 'http://211.159.149.56/sbsm/supermap/login.do'
# response = session.post(url, data=data, headers=headers)
# response.encoding = response.apparent_encoding
# rep = response.text
# print(response.status_code)
#
# with open('中国版图1.html', 'w', encoding='utf-8') as f:
#     f.write(rep)
