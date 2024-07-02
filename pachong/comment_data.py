"""
[课程内容]: Python采集B站视频评论数据加密参数逆向分析, 实现可视化分析

[授课老师]: 青灯教育-自游  [上课时间]: 20:05 可以点歌 可以问问题

[环境使用]:
    Python 3.10
    Pycharm
[模块使用]:
- 爬虫模块
  - requests / csv / hashlib / time / json / urllib
- 数据分析模块
  - pandas / pyecharts / jieba / wordcloud
需要安装的模块: requests pandas pyecharts jieba wordcloud
---------------------------------------------------------------------------------------------------
win + R 输入cmd 输入安装命令 pip install 模块名 (如果你觉得安装速度比较慢, 你可以切换国内镜像源)
先听一下歌 等一下后面进来的同学,20:05正式开始讲课 [有什么喜欢听得歌曲 也可以在公屏发一下]
相对应的安装包/安装教程/激活码/使用教程/学习资料/工具插件 可以加婧琪老师微信python1018
---------------------------------------------------------------------------------------------------

"""
import pandas as pd
# 导入数据请求模块 (需要安装 pip install requests)
import requests
# 导入csv模块 (内置模块, 不需要安装)
import csv
# 导入哈希模块
import hashlib
# 导入json模块
import json
# 导入时间模块
import time
# 导入编码模块
from urllib.parse import quote


def GetData(date_time, page):
    pagination_str = '{"offset":%s}' % page
    print(quote(pagination_str))
    # 传入参数列表
    ee = [
        "mode=3",
        "oid=112676873175571",
        f"pagination_str={quote(pagination_str)}",
        "plat=1",
        "type=1",
        "web_location=1315875",
        f"wts={date_time}"
    ]

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
    print(w_rid)
    return w_rid


def GetContent(next_param, oid):
    """发送请求"""
    # 模拟浏览器
    headers = {
        # User-Agent 用户代理, 表示浏览器基本身份信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    # 请求网址
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main'
    # 获取时间戳
    date_time = int(time.time())
    # 获取加密参数
    w_rid = GetData(date_time=date_time, page=next_param)
    # 查询参数
    data = {
        'oid': '112676873175571',
        'type': '1',
        'mode': '2',
        'pagination_str': '{"offset":%s}' % next_param,
        'plat': '1',
        'web_location': '1315875',
        'w_rid': w_rid,
        'wts': date_time,
    }
    # 发送请求
    response = requests.get(url=url, params=data, headers=headers)
    """获取数据"""
    # 获取响应json数据
    json_data = response.json()
    json_dumps = json.dumps(json_data, ensure_ascii=False, indent=4)
    with open('data.txt', 'w', encoding='utf-8') as file:
        file.write(json_dumps)
    """解析数据"""
    # 提取评论信息所在列表 (20条评论信息内容)
    replies = json_data['data']['replies']
    # for循环遍历, 提取列表里面元素
    for index in replies:
        # 根据键值对, 提取具体数据内容, 保存到字典
        dit = {
            '昵称': index['member']['uname'],
            '性别': index['member']['sex'],
            '地区': index['reply_control'].get('location', '').replace('IP属地：', ''),
            '评论': index['content']['message'],
        }
        # 写入数据
        csv_writer.writerow(dit)
        print(dit)
    # 获取下一页的参数内容
    next_param = json.dumps(json_data['data']['cursor']['pagination_reply']['next_offset'])
    print(next_param)
    return next_param

if __name__ == '__main__':
    # 创建文件对象
    f = open('data.csv', mode='w', encoding='utf-8', newline='')
    # 字典写入方法
    csv_writer = csv.DictWriter(f, fieldnames=['昵称', '性别', '地区', '评论'])
    # 写入表头
    csv_writer.writeheader()
    next_param = '""'
    metadata = pd.read_csv('related_video_data_2_new.csv')
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_colwidth', None)  # Show full column width
    pd.set_option('display.expand_frame_repr', False)  # Prevent truncation

    metadata = metadata.iloc[:, 1:8]
    metadata = metadata.drop_duplicates(subset=['oid'])
    print(metadata.head())
    for index,row in metadata.iterrows():
        title = row['meta_full_title']
        oid = row ['oid']
        author = row['meta_author']
        play = row['meta_playbacks']

        for page in range(1, 21):
            next_param = GetContent(next_param=next_param, oid=oid)