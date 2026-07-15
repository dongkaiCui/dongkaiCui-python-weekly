import requests
from bs4 import BeautifulSoup
import time
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_helper import MySQLHelper

class DoubanMovieSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://movie.douban.com/'
        }
        self.db = MySQLHelper(database="spider_db")
        self.cursor = self.db.cursor
        self.conn = self.db.conn
        self.movies = []
        self.total = 0

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS douban_top100 (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(100) NOT NULL,
                rating DECIMAL(3,1) NOT NULL,
                director VARCHAR(100),
                actors VARCHAR(300),
                year INT,
                country VARCHAR(50),
                genres VARCHAR(100),
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def clear_table(self):
        self.cursor.execute('TRUNCATE TABLE douban_top100')
        self.conn.commit()

    def parse_movie(self, li):
        title_tag = li.select_one('.title')
        title = title_tag.text.strip() if title_tag else ''
        rating_tag = li.select_one('.rating_num')
        rating = float(rating_tag.text.strip()) if rating_tag else 0.0
        info_tag = li.select_one('.bd p')
        director = ''
        actors = ''
        year = 0
        country = ''
        genres = ''
        if info_tag:
            text = info_tag.get_text(strip=True)
            year_match = re.search(r'\b(\d{4})\b', text)
            if year_match:
                year = int(year_match.group(1))
            if '导演:' in text:
                director = text.split('导演:')[1].split(' ')[0].strip()
            if '主演:' in text:
                actors = text.split('主演:')[1].split(' ')[0].strip()
            if year != 0:
                year_pos = text.find(str(year))
                if year_pos != -1:
                    rest = text[year_pos + len(str(year)):].strip()
                    if '/' in rest:
                        parts = rest.split('/')
                        if len(parts) >= 2:
                            country = parts[1].strip()
                        if len(parts) >= 3:
                            genres = parts[2].strip()
        return {
            'title': title,
            'rating': rating,
            'director': director,
            'actors': actors,
            'year': year,
            'country': country,
            'genres': genres
        }

    def fetch_page(self, page):
        start = page * 25
        url = f'https://movie.douban.com/top250?start={start}&filter='
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('ol.grid_view li')
        for li in items:
            movie = self.parse_movie(li)
            self.movies.append(movie)

    def fetch_all(self):
        for page in range(4):
            self.fetch_page(page)
            time.sleep(1)

    def save_to_db(self):
        self.create_table()
        self.clear_table()
        for m in self.movies:
            sql = '''
                INSERT INTO douban_top100 (title, rating, director, actors, year, country, genres)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            self.cursor.execute(sql, (m['title'], m['rating'], m['director'], m['actors'],
                                      m['year'], m['country'], m['genres']))
            self.total += 1
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def run(self):
        print('正在爬取豆瓣电影Top100...')
        self.fetch_all()
        self.save_to_db()
        print(f'全部完成！共入库 {self.total} 部电影，表名：douban_top100')
        self.close()

if __name__ == '__main__':
    spider = DoubanMovieSpider()
    spider.run()