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
order_data = '{"campus_id":1,"area_id":1,"building_id":,"room_number":"","barrel_id":888,"password":"","send_num":1,"phone":""}'


def login():
    global homeUrl
    session = requests.session()
    html = session.get(loginUrl).content.decode('utf-8')
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    cookies = {"languageIndex": "0", "last_oauth_appid": "illnessProtectionHome", "last_oauth_state": "home"}
    pattern = re.compile(r"var token = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
    data = {'username': username, 'password': password, '__token__': pattern.search(html).group(1),
            'wechat_verif': ''}
    response = json.loads(session.post(url=loginUrl, headers=headers, cookies=cookies, data=data).json())
    session.close()
    if response['message'] != '验证通过':
        console_msg('登录验证失败', 1)
        return 1
    console_msg('登录验证成功', 0)
    homeUrl = response['info']
    console_msg('homeUrl: \'' + homeUrl + '\'', 0)
    return 0


def order():
    session = requests.session()
    html = session.get(url=homeUrl)
    session.get(html.url)
    pattern = re.compile(r"token=(.*?)$", re.MULTILINE | re.DOTALL)
    token = pattern.search(html.url).group(1)
    console_msg('token: \'' + token + '\'', 0)
    headers = {'Host': 'ehall.dgut.edu.cn', 'Referer': 'http://ehall.dgut.edu.cn/WaterBookP',
               'Origin': 'http://ehall.dgut.edu.cn', 'Content-type': 'application/json; charset=utf-8',
               'Accept-Encoding': 'gzip, deflate', 'Cookie': 'PHPSESSID=' + token, 'authorization': token}
    response = session.post(url='http://ehall.dgut.edu.cn/hq/home/Distribution/addDistribution.hq', headers=headers,
                            data=order_data)
    print(response.content.decode('utf-8'))


def console_msg(msg, level=2):
    header = ('[SUCCESS]', '[ERROR]', '[INFO]')
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
