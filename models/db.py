"""
 @Author: 西琳
 @FileName: db.py
 @DateTime: 2024/9/18 下午7:54
 @SoftWare: PyCharm
"""
import pymysql
from flask import current_app


def get_db_conn():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='db',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"数据库连接失败: {e}")
        return None


def fetch_single_record(query, params):
    conn = get_db_conn()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        conn.close()
        return result
    return None


def fetch_multiple_records(query, params=None):
    conn = get_db_conn()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params) if params else cursor.execute(query)
            results = cursor.fetchall()
        conn.close()
        return results
    return []


def get_post_from_db(post_id):
    conn = get_db_conn()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
            result = cursor.fetchone()
        conn.close()
        return result
    return None
