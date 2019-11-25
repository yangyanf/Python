import random
import time
import requests
from bs4 import BeautifulSoup
import pymysql.cursors
#设计在线 http://www.dolcn.com/archives/category/competitions/page
def get_conn():
    '''建立数据库连接'''
    conn = pymysql.connect(host='localhost',user='root',password='root',db='python',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    return conn

def insert(conn, info):
    '''数据写入数据库'''
    with conn.cursor() as cursor:
        sql = "INSERT INTO `sj_user_activity` (`title`, `cover_img`, `content`, `uid`,`user_type`,`status`, `act_status`,`tags_code`,`area_code`,`cate_id`, `address`,`create_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        rseult = cursor.execute(sql, info)
        conn.commit()
        return rseult
def get_article_href(html):
    soup = BeautifulSoup(html, 'html.parser')
    act_list = soup.find('div', attrs={'id': 'content'})
    act_href = []
    for i in act_list.find_all('article'):
        href = i.find('h1', attrs={'class': 'entry-title'}).find('a').get("href")
        act_href.append(href)
    return act_href
def get_html(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    html = requests.get(url, headers=header).content
    return html
def get_html_value(html):
    soup = BeautifulSoup(html, 'html.parser')

    acticle = soup.find('article') #获取文章
    #背景图
    cover_img = acticle.find('img')
    if cover_img is None:
        cover_img = ''
    else:
        cover_img = cover_img.get("src")
    content = acticle.find('div', attrs={'class': 'entry-content'})#获取文章内容
    uidArr = [553,554,581,586,629,871,904,905,906,908,909,911,916,917,919,923,927,928,931,933,935,936,937,938,940,941,943,944,945,946,947,1589,1607,1608,1609,1610,1611,1613,1614]
    randomNumber = random.randint(0, len(uidArr) - 1)
    row = [
        acticle.find('h1', attrs={'class': 'entry-title'}).get_text(),#标题
        cover_img,  #背景图
        str(content),  # 内容
        uidArr[randomNumber],  # 用户编号 随机一个系统用户
        1,  # 用户类型
        1,  # 审核状态通过
        1,  # 活动状态 进行中
        2,  # 标签 {1：活动 2：赛事 3：展览 4：项目}
        '', # 地区
        '', # 分类
        '', # 地址
        int(time.time()),
    ]
    return row
def main():
    # i = 'http://www.dolcn.com/archives/18697'
    # html = get_html(i)
    # row = get_html_value(html)
    # print(row)
    # exit()
    name_list = [] #各个活动链接地址
    for i in range(1, 35):#获取1-34 页数据
        url = "http://www.dolcn.com/archives/category/competitions/page/"+ str(i)
        html = get_html(url)
        href = get_article_href(html)
        name_list = name_list + href
    print(len(name_list))
    conn = get_conn()

    for i in name_list:
        print(i)
        html = get_html(i)
        row = get_html_value(html)
        result = insert(conn, tuple(row))  # 插入数据库
        print(result)

if __name__ == '__main__':
    main()