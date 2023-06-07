import pymysql

conn = pymysql.connect(host='localhost', user='root', password='0000', db='dbProject')
curs = conn.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM student"
curs.execute(sql)
rows = curs.fetchall()

for row in rows:
    print(row)

curs.close()
conn.close()
