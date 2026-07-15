import pymysql

class MySQLHelper:

    def __init__(
        self,
        host='localhost',
        user='root',
        password='qaz92451888',
        database='student_db',
        charset='utf8'
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )
        self.cursor = self.conn.cursor()

    def execute(self, sql, data=None):
        self.cursor.execute(sql, data)

        if sql.strip().lower().startswith("select"):
            return self.cursor.fetchall()

        self.conn.commit()
        return self.cursor.rowcount

    def close(self):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()