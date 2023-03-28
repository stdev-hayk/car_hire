import pymysql
import mysql.connector

from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB_NAME

cmx = mysql.connector.connect(
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    database=MYSQL_DB_NAME
)


def cursor_connection(sql, data, view):
    row = rows = []
    cmx.connect()
    if view in ('users', 'edit_user'):
        cursor = cmx.cursor(pymysql.cursors.DictCursor)
    else:
        cursor = cmx.cursor()
    cursor.execute(sql, data)
    if view == 'users':
        rows = cursor.fetchall()
    elif view == 'edit_user':
        row = cursor.fetchone()
    else:
        cmx.commit()

    cursor.close()
    cmx.close()

    return row, rows
