import random
import time
import requests
import re
import pydoc
from bs4 import BeautifulSoup
import pymysql.cursors
# 世界最受欢迎的建筑网站   https://www.archdaily.cn/cn/search/competitions?ad_name=main-menu
def get_conn():
    '''建立数据库连接'''
    conn = pymysql.connect(host='localhost',user='root',password='root',db='python',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    return conn

def insert(conn, info):
    '''数据写入数据库'''
    with conn.cursor() as cursor:
        sql = "INSERT INTO `sj_user_activity4` (`title`, `cover_img`, `content`, `uid`,`user_type`,`status`, `act_status`,`tags_code`,`area_code`,`cate_id`, `address`,`begin_time`,`end_time`,`create_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        rseult = cursor.execute(sql, info)
        conn.commit()
        return rseult
#获取列表页数据
def get_list_row(html):
    soup = BeautifulSoup(html, 'html.parser')
    act_list = soup.find('ul', attrs={'class': 'afd-search-list--wrap'})
    #获取对应数据
    act_title = []#标题
    act_href = []#文章链接地址
    act_img = []#封面图
    for i in act_list.find_all('li'):
        title = i.find('h2').get_text()
        href = i.find('a', attrs={'class': 'afd-search-list__link'}).get("href")
        cover_img = i.find('img').get("src")

        act_title.append(title)
        act_href.append("https://www.archdaily.cn/"+href)
        cover_img = cover_img.replace("small_jpg", "newsletter", 2)
        act_img.append(cover_img)
        # print(act_title)
        # print(act_href)
        # print(act_img)
        # exit()
    return act_title,act_href,act_img
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    # re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    # s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    # s = replaceCharEntity(s)  # 替换实体
    return s
#获取文章内容
def get_article_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    info = [s.extract() for s in soup('figure')]#删除figure 页面
    info = [s.extract() for s in soup('div', attrs={'class': 'article-meta'})]#删除div
    # print(info)
    content = soup.find('article', attrs={'id': 'single-content'}) # 获取文章内容
    content = str(content)
    # acc = content.split('<!-- 分页条 -->')
    # content =  acc[0]
    content = filter_tags(content) #去除css
    print(content)
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
    # range(range(4,1,-1))
    for i in range(4,0,-1):#获取4-1 页数据
        url = "https://www.archdaily.cn/cn/search/competitions?page="+str(i)
        html = get_html(url)
        title_row,href_row,img_row = get_list_row(html)#标题 内容链接 图片 数组

        for j in range(len(href_row),1,-1):
            conn = get_conn()
            html = get_html(href_row[j-1])
            content = get_article_content(html)
            uidArr = [553, 554, 581, 586, 629, 871, 904, 905, 906, 908, 909, 911, 916, 917, 919, 923, 927, 928, 931,
                      933, 935, 936, 937, 938, 940, 941, 943, 944, 945, 946, 947, 1589, 1607, 1608, 1609, 1610, 1611,
                      1613, 1614]
            randomNumber = random.randint(0, len(uidArr) - 1)

            row = [
                title_row[j],  # 标题
                img_row[j],  # 背景图
                content,  # 内容
                uidArr[randomNumber],  # 用户编号 随机一个系统用户
                1,  # 用户类型
                1,  # 审核状态通过
                1,  # 活动状态 1:进行中 2:已结束
                2,  # 标签 {1：活动 2：赛事 3：展览 4：项目}
                '',  # 地区
                132,  # 分类
                '',  # 地址
                0,  # 开始时间
                0,  # 结束时间
                int(time.time()),
            ]
            print(row)
            # exit()
            result = insert(conn, tuple(row))  # 插入数据库
            print(result)

if __name__ == '__main__':
    main()