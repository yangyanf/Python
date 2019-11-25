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
def download_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    return r.text

def main():

    url_parse = "https://www.linkedin.com/directory/companies-a-{}"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    for x in range(1, 2):
        s = requests.Session()
        cookie = 'v=2&1f4dcb38-ff90-4432-8df9-f982db5a1958"; bscookie="v=1&201907110358547df19e1f-a0e1-46b9-8d2d-daba17e7b7b3AQEz3FvmM8eC9lfoYekyoEVWd1hZeQyw"; _ga=GA1.2.852361488.1562817560; aam_uuid=59938095213646499250540233689460650472; JSESSIONID=ajax:1493445896428407965; lang=v=2&lang=zh-cn; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-1303530583%7CMCIDTS%7C18107%7CMCMID%7C60442234851715778700554053328518169123%7CMCAAMLH-1564998246%7C11%7CMCAAMB-1564998246%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1564400646s%7CNONE%7CvVersion%7C3.3.0; lissc1=1; lissc2=1; fid=AQH8rio0pZz_0gAAAWw9ICD1mSQoxf4q4QijgEYOAKPOfA0Txb9lbzmeZJNHKcXIB-vglMPwGgzhng; fcookie=AQFnNFYIrUbZwgAAAWw9ICylo8lm7ALhSyzTEYxKKUqFTreOZnkL1sAvo1Sie3I2osDDLAxNxF6hRSa2p_D9kO0EIXrQwO2ciO-MUZewPXSam4AIo79w-X633QeYBN3H6lKIcAi-LklTGcSF0PI9M1cALrOywJodjE9iff1IXupbl9Kx9x0uaAO5Ua81QA-HcdG5RRwoC-hN8pgi4xtmwMumWtcSxIpvbNNDwgaP3xbd5hUJ1Wz0juwdX_BzVAn0Jwu9AEpP0qKhNLHTLud-bwgO40fG/WtlgRBrISY4AvCTH1EOycz/KUT+yymhe3JQx/mHp6qW1Ja2K8hIQPdhK9SAhM9eeVELRtkHvQ23vj4A==; sl=v=1&kB8Ta; liap=true; li_at=AQEDASz4HSQCjnUdAAABbD0g23gAAAFsYS1feFEAeiA4bZMd0ODDztna6V5MzPFB1szipAq5sKKs-BVigNAdr4j_0uDD5VDdf38zYxNyqTao0WOp5HacPWXpol41kOYqPiscpbWoBJ-Op7LlSpRBVfc5; wwepo=true; _lipt=CwEAAAFsPSDfmC_vOmmJVFLk75cye8GofhckU8XXpzikNHn8dMjKAbOVF-ybcQCM8mNyyymixAYvE32v82cMHmAnbm2cNuxim8e-cfVGAPCyT_u4R4LjFMU; li_cc=AQHwJ1mLym_ClgAAAWw9IN-2MDkuP5tWg5LKo1dRGxecxx9Al4pc7ePkeapyO0ml-2G-4EceC3-x; _guid=3f24499d-00b9-40ef-abfe-e79751b393bc; li_oatml=AQEcIkKqnne8dwAAAWw9IOQKeYynaCtTZsXuuNeQ5DZZ2n3voAq0d7S5AEutJSPLKEsAjnusIDCAjW2zUUw_UocI2Cv1PzZe; UserMatchHistory=AQKzYGmsMus8MgAAAWw9JiPpABXRKQaZfzjlV575XsKsWqXLcClRrv-AQgvUmZw4H3EZAFE-OlEqJgzMBPZ3Rl4OTqXhYKC_cEntfTLyZb88xl3DuenzOXDDzjr-1xbqXcxLe7mHPJnSXIFaGG1ehVwnZIdBillv_stpfiYviRfKdk72_z14Mc5UbpjlmGrvqyMb3V-Lc6CBFz2-h0rtaH3y7ZPAkAdQQzsu; _gat=1; lidc="b=SGST01:g=4:u=1:i=1564394348:t=1564480059:s=AQHbGfQVS8_ghnGmgfh4KI8oRrERhnj4'
        #请求获取数据
        text = download_page(url_parse.format(x))
        print(text)


if __name__ == '__main__':
    main()