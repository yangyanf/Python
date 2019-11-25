import random
import time
import requests
import re
import pydoc
from bs4 import BeautifulSoup
import pymysql.cursors
# 设计本   https://www.shejiben.com/event/t1/p1
# 奖项 https://www.shejiben.com/event/t1/p1
def get_conn():
    '''建立数据库连接'''
    conn = pymysql.connect(host='localhost',user='root',password='root',db='python',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    return conn

def insert(conn, info):
    '''数据写入数据库'''
    with conn.cursor() as cursor:
        sql = "INSERT INTO `sj_user_activity2` (`title`, `cover_img`, `content`, `uid`,`user_type`,`status`, `act_status`,`tags_code`,`area_code`,`cate_id`, `address`,`begin_time`,`end_time`,`create_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        rseult = cursor.execute(sql, info)
        conn.commit()
        return rseult
#获取列表页数据
def get_list_row(html):
    soup = BeautifulSoup(html, 'html.parser')
    act_list = soup.find('ul', attrs={'class': 'clearfix'})
    #获取对应数据
    act_title = []#标题
    act_href = []#文章链接地址
    act_img = []#封面图
    act_time = []#时间
    status = []#活动状态
    for i in act_list.find_all('li'):
        title = i.find('strong', attrs={'class': 'title'}).get_text()
        href = i.find('a').get("href")
        cover_img = i.find('img').get("src")
        time = i.find('div', attrs={'class': 'activity-info'}).find('span').get_text()
        print(time)
        status_text = i.find('span', attrs={'class': 'status'}).get_text()
        if status_text=='进行中':
            status.append(1)
        else:
            status.append(2)
        act_title.append(title)
        act_href.append("https://www.shejiben.com"+href)
        act_img.append(cover_img)
        act_time.append(time)
    return act_title,act_href,act_img,act_time,status
#获取文章内容
def get_article_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', attrs={'id': 'detail'}) # 获取文章内容
    # content = content.find_all('p')
    content = str(content)
    acc = content.split('<!-- 分页条 -->')
    content =  acc[0]
    # content = content.replace('<div class="col_zan clear"><div class="dianzan lf " data-identity="True" action-data="c5ca5a29-e70e-47a0-a285-aaed00feb237"><span class="dianzan_bg"></span><span>0</span></div><div class="shoucang lf " id="btnColl"><span class="shoucang_bg"></span><span>1</span></div></div>'," ")
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    s = re_style.sub('', content)  # 去掉style
    print(s)
    exit()
    return str(content)
#获取网页内容
def get_html(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    html = requests.get(url, headers=header).content
    return html
#运行main方法
def main():
    # i = 'http://www.dolcn.com/archives/18697'
    # html = get_html(i)
    # row = get_html_value(html)
    # print(row)
    # exit()
    name_list = [] #各个活动链接地址
    for i in range(1, 6):#获取1-18 页数据
        url = "https://www.shejiben.com/event/t1/p"+str(i)
        html = get_html(url)
        title_row,href_row,img_row,time_row,status_row = get_list_row(html)
        # print(title_row)
        # print(href_row)
        # print(img_row)
        # print(time_row)
        # print(status_row)
        for i in range(0,len(href_row)):
            conn = get_conn()
            html = get_html(href_row[i])
            content = get_article_content(html)
            uidArr = [553, 554, 581, 586, 629, 871, 904, 905, 906, 908, 909, 911, 916, 917, 919, 923, 927, 928, 931,
                      933, 935, 936, 937, 938, 940, 941, 943, 944, 945, 946, 947, 1589, 1607, 1608, 1609, 1610, 1611,
                      1613, 1614]
            randomNumber = random.randint(0, len(uidArr) - 1)
            act_time = time_row[i].split('-')
            row = [
                title_row[i],  # 标题
                img_row[i],  # 背景图
                content,  # 内容
                uidArr[randomNumber],  # 用户编号 随机一个系统用户
                1,  # 用户类型
                1,  # 审核状态通过
                status_row[i],  # 活动状态 1:进行中 2:已结束
                2,  # 标签 {1：活动 2：赛事 3：展览 4：项目}
                '',  # 地区
                132,  # 分类
                '',  # 地址
                int(time.mktime(time.strptime(act_time[0],'%Y.%m.%d'))),  # 开始时间
                int(time.mktime(time.strptime(act_time[1],'%Y.%m.%d'))),  # 结束时间
                int(time.time()),
            ]
            print(row)
            result = insert(conn, tuple(row))  # 插入数据库
            print(result)

if __name__ == '__main__':
    main()