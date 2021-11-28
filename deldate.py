from putinbase import BASELIST
from twd_psql import baseConnect
from getpass import getpass

passwd = getpass('Enter password')
dateToDel = '2020-07-03'
cur, conn = baseConnect('postgres', passwd)
for rec in BASELIST:
    cur.execute('ALTER TABLE "%s" DROP COLUMN "%s"' % (rec, dateToDel))
conn.commit()
cur.close()
conn.close()
