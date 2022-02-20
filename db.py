import pymysql

def db_connect():
    db = pymysql.connect(
        user='jwosnc',
        passwd='Jwosnc15677',
        host='jwosnc.cafe24.com',
        db='jwosnc',
        charset='utf8'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)

    return cursor, db
