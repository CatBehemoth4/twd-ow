import psycopg2
from getpass import getpass

passwd = getpass("Enter password:", )
connection = psycopg2.connect(dbname="TWD", user="postgres", password=passwd, host="194.67.105.168")
cursor = connection.cursor()
for i in range(1, 34):
    try:
        cursor.execute('ALTER TABLE zplayer%s ADD FOREIGN KEY ("group") REFERENCES "Groups"("Id");' % i)
        # connection.commit()
        # cursor.execute("""UPDATE zplayer%s SET "group" = 1 WHERE "dt" = '04/23/2020';""" % i)
    except:
        pass
    connection.commit()
connection.close()