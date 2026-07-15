import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_helper import MySQLHelper

class StudentManager:
    def __init__(self):
        self.db = MySQLHelper(database="student_db")

    def insert_student(self):
        self.db.execute("INSERT INTO student VALUES ('001', 'Kevin', 175)")

    def select_student(self):
        return self.db.execute("SELECT * FROM student")

    def update_student(self):
        self.db.execute("UPDATE student SET height = 180 WHERE id = '001'")

    def delete_student(self):
        self.db.execute("DELETE FROM student WHERE id = '001'")

    def run(self):
        print("1. 插入数据...")
        self.insert_student()

        print("2. 查询数据：")
        print(self.select_student())

        print("3. 更新身高为180...")
        self.update_student()

        print("4. 再次查询：")
        print(self.select_student())

        print("5. 删除记录...")
        self.delete_student()

        print("6. 最后查询：")
        print(self.select_student())

        self.db.close()

if __name__ == '__main__':
    manager = StudentManager()
    manager.run()