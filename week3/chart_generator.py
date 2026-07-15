import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_helper import MySQLHelper

class MovieChartGenerator:
    def __init__(self):
        self.db = MySQLHelper(database="spider_db")
        self.cursor = self.db.cursor
        self.conn = self.db.conn
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    def get_ratings(self):
        self.cursor.execute('SELECT rating FROM douban_top100')
        return [row[0] for row in self.cursor.fetchall()]

    def get_years(self):
        self.cursor.execute('SELECT year FROM douban_top100 WHERE year > 0')
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_movies(self):
        self.cursor.execute('SELECT title, rating FROM douban_top100 ORDER BY rating DESC')
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def show_rating_distribution(self):
        ratings = self.get_ratings()
        plt.figure(figsize=(6, 4))
        plt.hist(ratings, bins=10, color='skyblue', edgecolor='black')
        plt.title('豆瓣Top100评分分布')
        plt.xlabel('评分')
        plt.ylabel('电影数量')
        plt.show()

    def show_year_distribution(self):
        years = self.get_years()
        plt.figure(figsize=(6, 4))
        plt.hist(years, bins=range(1950, 2026, 5), color='lightgreen', edgecolor='black')
        plt.title('豆瓣Top100年份分布')
        plt.xlabel('年份')
        plt.ylabel('电影数量')
        plt.xticks(rotation=45)
        plt.show()

    def show_all_ratings(self):
        movies = self.get_all_movies()
        titles = [row[0] for row in movies]
        ratings = [row[1] for row in movies]
        plt.figure(figsize=(12, 40))
        bars = plt.barh(titles, ratings, color='skyblue', height=0.6)
        plt.xlabel('评分')
        plt.title('豆瓣Top100 全部电影评分排序（精确数值）')
        plt.gca().invert_yaxis()
        for bar, rating in zip(bars, ratings):
            plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                     f'{rating:.1f}', va='center', ha='left', fontsize=8)
        plt.tight_layout()
        plt.show()

    def save_all_ratings(self, filename='douban_top100_chart.png'):
        movies = self.get_all_movies()
        titles = [row[0] for row in movies]
        ratings = [row[1] for row in movies]
        fig, ax = plt.subplots(figsize=(12, 40))
        bars = ax.barh(titles, ratings, color='skyblue', height=0.6)
        ax.set_xlabel('评分')
        ax.set_title('豆瓣Top100 全部电影评分排序（精确数值）')
        ax.invert_yaxis()
        for bar, rating in zip(bars, ratings):
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{rating:.1f}', va='center', ha='left', fontsize=8)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        print(f'图表已保存为 {filename}')

    def show_all_charts(self):
        self.show_rating_distribution()
        self.show_year_distribution()
        self.show_all_ratings()

if __name__ == '__main__':
    chart = MovieChartGenerator()
    chart.save_all_ratings()  
    chart.close()