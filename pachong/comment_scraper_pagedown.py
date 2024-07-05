"""
删掉别人的介绍不会让代码变成我的，但的确跟他的差距很大了。
核心技术获取自：青灯教育 自游老师，我拿到的可能也是公众号的八百手资料
等我完全消化了可以出一个更dedicated的关于b站评论区的教学吧
"""
# 导入数据请求模块 (需要安装 pip install requests)
import requests
import numpy as np
# 导入csv模块 (内置模块, 不需要安装)
import csv
# 导入哈希模块
import hashlib
# 导入json模块
import json
# 导入时间模块
import time
import pandas as pd
# 导入编码模块
from urllib.parse import quote
import random

date_execution = '0705'
def GetData(date_time, page, oid):
    pagination_str = '{"offset":%s}' % page
    #print(quote(pagination_str))
    # 传入参数列表
    ee = [
        "mode=3",
        f"oid={oid}",
        f"pagination_str={quote(pagination_str)}",
        "plat=1",
        "type=1",
        "web_location=1315875",
        f"wts={date_time}"
    ]
    ### 和教的时候相比，这里的参数名字从ee变成en了，但数值没变，偷懒的反爬组
    # 把列表合并成字符串
    L = '&'.join(ee)
    # 字符串拼接
    string = L + "ea1db124af3c7062474693fa704f4ff8"
    # 调用md5加密算法
    MD5 = hashlib.md5()
    # 传入需要加密参数内容
    MD5.update(string.encode('utf-8'))
    # 进行md5加密处理
    w_rid = MD5.hexdigest()
    # print(w_rid)
    return w_rid


def GetContent(NextPage, oid):
    """发送请求"""
    # 模拟浏览器
    headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 需定期更换cookie，否则location爬不到
    'cookie': "buvid3=E579EDE8-64A3-72D3-AD0D-9A111BE54DD103395infoc; b_nut=1713522703; CURRENT_FNVAL=4048; _uuid=A410CC8A5-FF13-FF86-D6FA-3542F4CC4910F05666infoc; buvid4=346F68FE-9DBC-DD3B-F9B3-C82EF884743305819-024041910-AYCtu957i4E2ZljBHTFxVg%3D%3D; rpdid=|(uJ~l)lmJ~R0J'u~uJlkk~ul; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NEW_POP; header_theme_version=CLOSE; buvid_fp_plain=undefined; DedeUserID=37424969; DedeUserID__ckMd5=02c3aef233c2afc9; LIVE_BUVID=AUTO4617194323455968; PVID=2; CURRENT_QUALITY=0; fingerprint=e5891333f9ec39c7d8c141672ff5b516; buvid_fp=9e6e957ef938b008b39a95d392784574; home_feed_column=5; bp_t_offset_37424969=948823447520149504; SESSDATA=39c0a02f%2C1735663622%2C2a294%2A72CjBQ04wvuK3GCoxYXHsTHmxowjuhWpZ6kjABSL4SlUSpPcFV6eJFK0BEaOFDorX_OUgSVnVaWnkyVV91TmZCOC1PVXotQkQzclk4cVAwcHQ5WWdwTm9XYVhMU252dFplTm1GZ0hYMGZQMEJyM3ZiakVWT1JEY2pBU05KZzVPdm9fdWNKcTYxNWN3IIEC; bili_jct=962e6eb1bf48280cb23859fb9a8778b2; sid=6hc86u5l; b_lsid=4E4FD325_190800BC43D; browser_resolution=1707-940; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAzOTQ0MTcsImlhdCI6MTcyMDEzNTE1NywicGx0IjotMX0.UwiDHqUqMVDSGHn6rMThzXRA0ZULN2YhbZAEO7G3LP4; bili_ticket_expires=1720394357",
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/video/BV1FG4y1Z7po/?spm_id_from=333.337.search-card.all.click&vd_source=69a50ad969074af9e79ad13b34b1a548',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
}

    # 请求网址
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main'
    # 获取时间戳
    date_time = int(time.time())
    # 获取加密参数
    w_rid = GetData(date_time=date_time, page=NextPage, oid=oid)
    # 查询参数
    data = {
        'oid': oid,
        'type': '1',
        'mode': '3',
        'pagination_str': '{"offset":%s}' % NextPage,
        'plat': '1',
        'web_location': '1315875',
        'w_rid': w_rid,
        'wts': date_time,
    }
    # 发送请求
    response = requests.get(url=url, params=data, headers=headers)

    if response.status_code == 200:
        """获取数据"""
        # 获取响应json数据
        json_data_all = response.json()
        json_dump = json.dumps(json_data_all, ensure_ascii=False, indent=4)
        with open('data.txt', 'w', encoding='utf-8') as file:
            file.write(json_dump)

        """解析数据"""
        # 提取评论信息所在列表 (20条评论信息内容)
        replies = json_data_all.get('data', {}).get('replies', [])
        dits = []  # List to store all dit dictionaries
        # for循环遍历, 提取列表里面元素
        for index in replies:
            # 根据键值对, 提取具体数据内容, 保存到字典
            dit = {
                'username': index['member']['uname'],
                'sex': index['member']['sex'],
                'location': index['reply_control'].get('location', 'unknown').replace('IP属地：', ''),
                'text': index['content']['message'],
                'likes': index['like'],
                'time': index['reply_control']['time_desc']
            }
            dits.append(dit)

        # 获取下一页的参数内容
        try:
            NextPage = json.dumps(json_data_all['data']['cursor']['pagination_reply']['next_offset'])
        except KeyError:
            print("Next offset not found, exiting loop.")
            return None, dits

        return NextPage, dits
    else:
        print(f"Failed to fetch data: Status code {response.status_code}")
        retries -= 1
        time.sleep(random.uniform(5, 10))  # Wait before retrying
    return None, []

if __name__ == '__main__':
    # 创建文件对象
    with open(f'comment_data_3_{date_execution}.csv', mode='w', newline='', encoding='utf-8') as file:
        # Create a csv writer object
        csv_writer = csv.writer(file)
        csv_writer.writerow(['title', 'oid', 'author', 'play', 'username', 'sex', 'location', 'text', 'likes', 'time'])
        index_number = 0
        total_sleep_time = 0
        total_pages = 0
        dtype_spec = {3: str, 4: str}
        metadata = pd.read_csv('related_video_data_3_2024_07_04.csv', low_memory=False, dtype=dtype_spec)
        metadata.iloc[:, 7] = metadata.iloc[:, 7].astype(int)

        pd.set_option('display.float_format', '{:.0f}'.format)
        pd.set_option('display.max_columns', None)  # Show all columns
        pd.set_option('display.max_colwidth', None)  # Show full column width
        pd.set_option('display.expand_frame_repr', False)  # Prevent truncation

        metadata = metadata.iloc[:, 1:8]
        metadata = metadata.drop_duplicates(subset=['oid'])
        print(metadata.head())

        total_script_start_time = time.time()
        for index, row in metadata.iterrows():
            title = row['meta_full_title']
            oid = row['oid']
            author = row['meta_author']
            play = row['meta_playbacks']

            sleep = random.uniform(0.9, 1.9)
            time.sleep(sleep)
            print(f'sleeping for {sleep}')
            total_sleep_time = total_sleep_time + sleep

            index_number = index_number + 1
            print(f'slept for {total_sleep_time}')
            print(f'index = {index_number}')
            print(f'pages = {total_pages}')
            NextPage = '""'
            pages = 0
            while NextPage:
                NextPage, dits = GetContent(NextPage=NextPage, oid=oid)

                pages = pages + 1

                if pages % 10 == 0:
                    sleep = random.uniform(0.9, 1.9)
                    time.sleep(sleep)
                    print(f'waiting {sleep}s for next page')
                    total_sleep_time = total_sleep_time + sleep
                    print(f'slept for {total_sleep_time}')

                if dits:
                    for dit in dits:
                        csv_writer.writerow(
                            [title, oid, author, play, dit['username'], dit['sex'], dit['location'], dit['text'],
                             dit['likes'],
                             dit['time']])
                if NextPage is None:
                    total_pages = total_pages + pages
                    break
            total_script_end_time = time.time()  # End timing the entire script
            total_script_duration = total_script_end_time - total_script_start_time
            print(f'Total script execution time: {total_script_duration} seconds')
            print(f'Total sleep time: {total_sleep_time} seconds')