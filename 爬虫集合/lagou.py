import random
import time
import requests
from openpyxl import Workbook
import pymysql.cursors
import json

def get_conn():
    '''建立数据库连接'''
    conn = pymysql.connect(host='localhost',user='root',password='root',db='python',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    return conn

def insert(conn, info):
    '''数据写入数据库'''
    with conn.cursor() as cursor:
        sql = "INSERT INTO `company` (`shortname`, `fullname`, `industryfield`, `financeStage`,`companySize`,`positionName`, `salary`,`skillLables`,`city`, `education`,`time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, info)
        conn.commit()

def main():
    url_start = "https://www.lagou.com/jobs/list_运维?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?city=成都&needAddtionalResult=false"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    for x in range(1, 5):

        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        #第二次请求 获取数据
        data = {
            'first': 'true',
            'pn': str(x),
            'kd': '运维'
        }
        response = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
        time.sleep(5)
        response.encoding = response.apparent_encoding
        text = json.loads(response.text)
        info = text["content"]["positionResult"]["result"]
        wb = Workbook()  # 打开 excel 工作簿
        conn = get_conn()
        for i in info:
            row = [
                i["companyShortName"],#公司简称
                i["companyFullName"],#公司全称
                i["industryField"],#行业
                i["financeStage"],#融资信息
                i["companySize"],#公司规模
                i["positionName"],  # 职位
                i["salary"],#薪资
                i["skillLables"],#标签
                i["city"]+i["district"]+i["stationname"],#地区
                i["education"],
                i["createTime"],
            ]
            print(row)
            insert(conn,tuple(row)) #插入数据库
            wb.save('{}职位信息.xlsx'.format('python'))

if __name__ == '__main__':
    main()