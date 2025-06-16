import csv
import mysql.connector
from datetime import datetime


class MySQLHelper:
    def __init__(self, host='localhost', user='root', password='', database='mars'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print('[✓] MySQL 연결 성공')
        except mysql.connector.Error as err:
            print(f'[-] MySQL 연결 실패: {err}')

    def insert_weather_data(self, mars_date, temp, stom):
        try:
            sql = 'INSERT INTO mars_weather (mars_date, temp, stom) VALUES (%s, %s, %s)'
            self.cursor.execute(sql, (mars_date, temp, stom))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f'[-] 데이터 삽입 실패: {err}')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print('[*] 연결 종료')


def read_and_insert_csv(filepath, db_helper):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 스킵
            for row in reader:
                try:
                    mars_date = datetime.strptime(row[1], '%Y-%m-%d')
                    temp = int(float(row[2]))  # 실수 형태도 정수로 변환
                    stom = int(row[3])
                    db_helper.insert_weather_data(mars_date, temp, stom)
                except Exception as e:
                    print(f'[-] 행 변환 실패: {row} - {e}')
    except FileNotFoundError:
        print(f'[-] 파일 없음: {filepath}')


if __name__ == '__main__':
    db = MySQLHelper(
        host='localhost',
        user='root',
        password='dnftiavn1001*',  # 비밀번호에 맞게 수정
        database='mars'
    )
    db.connect()
    read_and_insert_csv('mars_weathers_data.csv', db)
    db.close()
