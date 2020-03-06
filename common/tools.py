import json

import requests
import pymysql


# resp = requests.put('http://120.77.222.217:9200/zufang/')
# print(resp.text)

# conn = pymysql.connect(host='120.77.222.217', port=3306,
#                        database='zufang', charset='utf8',
#                        user='luohao', password='Luohao.618',
#                        cursorclass=pymysql.cursors.DictCursor)
# with conn.cursor() as cursor:
#     cursor.execute('select houseid, title, detail, street from tb_house_info')
#     for houseinfo in cursor.fetchall():
#         url = f'http://120.77.222.217:9200/zufang/houseinfos/{houseinfo["houseid"]}/'
#         resp = requests.post(
#             url=url,
#             headers={
#                 'content-type': 'application/json'
#             },
#             data=json.dumps({
#                 'houseid': houseinfo['houseid'],
#                 'title': houseinfo['title'],
#                 'detail': houseinfo['detail'],
#                 'stree': houseinfo['street']
#             })
#         )
#         print(resp.text)

# keyword = input('输入搜索关键词: ')
# resp = requests.get(
#     url=f'http://120.77.222.217:9200/zufang/houseinfos/_search?q={keyword}',
# )
# print(resp.text)

# resp = requests.post(
#     url='http://120.77.222.217:9200/_analyze/',
#     headers={
#         'content-type': 'application/json'
#     },
#     data=json.dumps({
#         'analyzer': 'ik_smart',
#         'text': '中国男足在2022年卡塔尔世界杯预选赛中勇夺小组最后一名'
#     })
# )
# print(resp.text)
