# encoding:gbk
import requests
from fake_useragent import UserAgent
from YDMHTTPUbil import YDMHttp

def checkValidCode(fileName, codeType):
    # �û���
    username = 'qz_cai'

    # ����
    password = 'cai_201314'

    # ����ɣģ������߷ֳɱ�Ҫ��������¼�����ߺ�̨���ҵ��������ã�
    appid = 10525

    # �����Կ�������߷ֳɱ�Ҫ��������¼�����ߺ�̨���ҵ��������ã�
    appkey = '30c380d8645c5b722dbcdc979efa4f8a'

    # ͼƬ�ļ�
    filename = fileName

    # ��֤�����ͣ�# ����1004��ʾ4λ��ĸ���֣���ͬ�����շѲ�ͬ����׼ȷ��д������Ӱ��ʶ���ʡ��ڴ˲�ѯ�������� http://www.yundama.com/price.html
    codetype = codeType

    # ��ʱʱ�䣬��
    timeout = 60

    # ���
    if (username == 'username'):
        print('�����ú���ز����ٲ���')
    else:
        # ��ʼ��
        yundama = YDMHttp(username, password, appid, appkey)

        # ��½�ƴ���
        uid = yundama.login();
        print('uid: %s' % uid)

        # ��ѯ���
        balance = yundama.balance();
        print('balance: %s' % balance)

        # ��ʼʶ��ͼƬ·������֤������ID����ʱʱ�䣨�룩��ʶ����
        cid, result = yundama.decode(filename, codetype, timeout);
        print('cid: %s, result: %s' % (cid, result))
        return result

headers = {
    'User-Agent': str(UserAgent().random)
}
session = requests.Session()

# �����֤��
img_url = 'http://211.159.149.56/sbsm/supermap/codeImg.do'
img_response = session.get(img_url, headers=headers)
img_response.encoding = img_response.apparent_encoding
img_rep = img_response.content
# print(img_response.status_code)

# ������֤��
with open('code.jpg', 'wb') as f:
    f.write(img_rep)

code = checkValidCode('code.jpg', 1004)
print(code)

# # img_code = input("��������֤��: ")
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
# with open('�й���ͼ1.html', 'w', encoding='utf-8') as f:
#     f.write(rep)
