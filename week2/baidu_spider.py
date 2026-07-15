import requests
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_helper import MySQLHelper

class BaiduHotSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.baidu.com/'
        }
        self.url = 'https://top.baidu.com/board?tab=realtime'

        # 指定连接 spider_db 数据库
        self.db = MySQLHelper(database="spider_db")

        self.hot_list = []

    def fetch(self):
        resp = requests.get(self.url, headers=self.headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        for div in soup.find_all('div', class_=lambda c: c and 'category-wrap' in c):
            title_tag = div.find('div', class_=lambda c: c and 'ellipsis' in c)
            score_tag = div.find('div', class_=lambda c: c and ('hot' in c.lower() or 'index' in c.lower()))

            if title_tag:
                title = title_tag.get_text(strip=True)
                score = score_tag.get_text(strip=True) if score_tag else '未知'
                self.hot_list.append((title, score))

            if len(self.hot_list) >= 10:
                break

    def create_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS baidu_hot (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(200),
                hot_score VARCHAR(50),
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.db.execute(sql)

    def clear_table(self):
        self.db.execute("TRUNCATE TABLE baidu_hot")

    def save_to_db(self):
        self.create_table()
        self.clear_table()

        for title, score in self.hot_list:
            self.db.execute(
                "INSERT INTO baidu_hot (title, hot_score) VALUES (%s, %s)",
                (title, score)
            )

    def run(self):
        print("正在爬取百度热搜...")
        self.fetch()

        print(f"抓到 {len(self.hot_list)} 条热搜")

        if self.hot_list:
            self.save_to_db()
            print("百度热搜入库成功")
        else:
            print("未抓到数据")

        self.db.close()

if __name__ == "__main__":
    spider = BaiduHotSpider()
    spider.run()