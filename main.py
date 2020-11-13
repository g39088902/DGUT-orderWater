import requests
import json
import sys
import re
import time

# Global Params
username = ''
password = ''
loginUrl = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/ehall/state/home.html'
homeUrl = ''
orderUrl = 'http://cas.dgut.edu.cn/hq/home/Pay/checkPay.hq'
#以下中文内容和要改，barrel_id是指不同品牌规格的桶装水，默认888为16.8L观音山
order_data = {"campus_id": 1, "area_id": 1, "building_id": 建筑id, "room_number": 房间号, "barrel_id": 888, "password": "", "send_num": 1, "phone": 手机号}


def login():
    global homeUrl
    session = requests.session()
    html = session.get(loginUrl).content.decode('utf-8')
    pattern = re.compile(r"var token = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
    data = {'username': username, 'password': password, '__token__': pattern.search(html).group(1),
            'wechat_verif': ''}
    console_msg('开始登录验证...', 2)
    response = json.loads(session.post(url=loginUrl, data=data).content.decode('utf-8'))
    session.close()
    if response['message'] != '验证通过':
        console_msg('登录验证失败', 1)
        return 1
    console_msg('登录验证成功', 0)
    homeUrl = response['info']
    return 0


def order():
    session = requests.session()
    html = session.get(url=homeUrl)
    session.get(html.url)
    console_msg('发送订水请求...')
    response = json.loads(session.post(url='http://ehall.dgut.edu.cn/hq/home/Distribution/addDistribution.hq',
                                       data=order_data).content.decode('utf-8'))
    if response['message'] == '订水成功，请等待配送':
        console_msg(response['message'], 0)
    elif response['message'] == '账户余额不足':
        console_msg(response['message'], 2)
    elif response['message'] == '桶装水正在配送中，您暂时无法再订购桶装水了。':
        console_msg(response['message'], 2)
    else:
        console_msg(response['message'], 1)


def console_msg(msg, level=2):
    header = (
        '[SUCCESS]',
        '[ERROR  ]',
        '[INFO   ]'
    )
    color = ("\033[32;1m", "\033[31;1m", "\033[36;1m")
    print(color[level], header[level], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg + "\033[0m")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        console_msg("参数出错", 1)
        console_msg(sys.argv[0] + " <username> <password>")
        exit(1)
    else:
        console_msg("Username: " + sys.argv[1])
        console_msg("Password: " + sys.argv[2])
        username = sys.argv[1]
        password = sys.argv[2]

    if login() != 0:
        console_msg('登录失败, 退出程序', 1)
        exit(1)
    # try:
    #     order()
    # except requests.exceptions.ConnectionError:
    #     console_msg('连接错误', 1)
    order()
