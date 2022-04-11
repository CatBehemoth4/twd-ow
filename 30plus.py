import psycopg2, json, datetime
from flask import Flask, make_response, request
from getpass import getpass
from putinbase import BASELIST

app = Flask(__name__)

def baseconnect(passwd):
    connection = psycopg2.connect(dbname="TWD", user="postgres", password='Ly)vwW-D2.c)o0Hp', host="localhost")
    cursor = connection.cursor()
    return cursor, connection

def downToThursday(dt, mode):
    wkd = dt.weekday()
    if (wkd != 3) | ((wkd == 3) & (dt.hour < 15) & mode):
        wkd += 7
        if ((wkd == 10) & (dt.hour < 15) & mode):
            wkd -= 1
            dt -= datetime.timedelta(1)
        while wkd % 7 != 3:
            wkd -= 1
            dt -= datetime.timedelta(1)
    return dt

def mindate(plr, mode=0):
    cur, conn = baseconnect(passw)
    # cur.execute('SELECT "Id" FROM "players" WHERE "Name" = \'%s\'' % plr)
    # idUsr = cur.fetchall()[0][0]
    cur.execute('SELECT * FROM "teams" WHERE "player" = %s' % plr)
    dats = cur.fetchall()[0]
    colmns = [desc[0] for desc in cur.description]
    datstot = list()
    for i in range(1, len(dats)):
        if dats[i] != None:
            datstot.append(colmns[i])
    datstot.sort(key=lambda x: x)
    if mode == 1:
        return datstot
    return datstot[0]


# @app.route('/')
# def rfr():
#    print(request)
#     a = request.data
#     print(a)
#     ret = json.dumps({'tr': (1, 2, 3)})
#     resp = make_response(ret)
#     resp.status_code = 200
#     resp.mimetype = 'application/json'
#     return resp

@app.after_request
def arq(req):
    # just init
    ret = json.dumps({'1': '1'})
    # receive data from request
    if request.method != 'OPTIONS':
        a = json.loads(request.data)
        # season list requested (a[0] = 1)
        if a[0] == 1:
            cur, conn = baseconnect('123')
        # taking all season's table from server
            cur.execute('SELECT * FROM "seasons" ORDER BY "Id" DESC')
            seasons = cur.fetchall()
        # formatting data to make them sendable
            seasonsRet = list()
            i = 0
            for rec in seasons:
                seasonsRet.append([rec[0], rec[1], str(rec[2]), str(rec[3]), str(rec[4]), str(rec[5]),
                                   str(rec[6]), str(rec[7]), str(rec[8]), rec[9]])
                i += 1
        # making json
            ret = json.dumps(seasonsRet)
            conn.close()
        # current players list requested (a[0] = 2)
        if a[0] == 2:
        # takind today's date
            dt = datetime.datetime.today()
            dt = downToThursday(dt, True)
        # counting down to nearest thursday (if today is thursday - counting down to previous if time is less than 3 p. m.
            rqstdt = dt.strftime("%Y-%m-%d")
        # taking player's ids from server
            cur, conn = baseconnect(passw)
            cur.execute('SELECT "player" FROM "teams" WHERE "%s" = 5' % rqstdt)
            idplrs = cur.fetchall()
        # taking players names from server
            cur.execute('SELECT "Id", "Name" FROM "players"')
            nicks = cur.fetchall()
            plrsRet = list()
            plrsRet0 = list()
        # connecting names with ids
            for num in idplrs:
                for nk in nicks:
                    if num[0] == nk[0]:
                        if len(mindate(num, mode=1)) > 1:
                            plrsRet.append([nk[0], nk[1]])
                            plrsRet0.append(nk[1])
            plrsRet0.sort(key=str.casefold)
            plrsRet.append(plrsRet0)
        # making json
            ret = json.dumps(plrsRet)
            conn.close()
        # requested data on special season (second in array) and week ((a[0] = 3))
        if a[0] == 3:
            cur, conn = baseconnect(passw)
            cur.execute('SELECT * FROM "seasons" WHERE "Id" = %s' % a[1])
            rec = cur.fetchall()
            rec = rec[0]
        # initiate dates of week start and finish
            stDat = rec[a[2] + 1]
            fiDat = rec[a[2] + 2]
        # if week is the last in season add 1 to finish date
            if a[2] == rec[9]:
                fiDat = rec[8]
                fiDat += datetime.timedelta(1)
            stDat = stDat.strftime("%Y-%m-%d")
            fiDat = fiDat.strftime("%Y-%m-%d")
        # receive players list which started and finished current week
            cur.execute('SELECT player FROM "teams" WHERE "%s" = 5 AND "%s" = 5' % (stDat, fiDat))
            plrs = cur.fetchall()
            plrs1 = list()
            for tupls in plrs:
                plrs1.append(tupls[0])
            tots = dict()
            for ids in plrs1:
                tots[ids] = []
        # receive data for players above at start and finish week for each table in base
            for base in BASELIST:
                for ids in plrs1:
                    cur.execute('SELECT "%s", "%s" FROM "%s" WHERE "player" = %s' % (stDat, fiDat, base, ids))
                    l = cur.fetchall()
                    # add result to the table
                    tots[ids].append(l[0][1] - l[0][0])
        # receive players names from server
            nams = dict()
            for ids in plrs1:
                cur.execute('SELECT "Name" FROM "players" WHERE "Id" = %s' % ids)
                nams[ids] = cur.fetchall()[0][0]
        # creatind resulting table
            resTable = list()
            for first in nams:
                row = list()
                row.append(nams[first])
                for cyph in tots[first]:
                    row.append(cyph)
                resTable.append(row)
        # sorting descending the table first by walkers killed
            resTable = sorted(resTable, key=lambda row: row[1], reverse=True)
        # sorting descending the table first by mission completed
            resTable = sorted(resTable, key=lambda row: row[4], reverse=True)
        # creating total row
            row1 = list()
            row1.append('Total')
            for i in range(1, len(resTable[0])):
                row1.append(0)
            for row in resTable:
                for i in range(1, len(row)):
                    row1[i] += row[i]
            resTable.append(row1)
        # making json
            ret = json.dumps(resTable)
            conn.close()
        # requested possible weeks of players
        if a[0] == 4:
            mindat = mindate(a[1])
            ret = json.dumps(mindat)
        if a[0] == 5:
            cur, conn = baseconnect(passw)
            nick = a[1]
            date1 = a[2]
            date2 = a[3]
            date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
            date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
            m = datetime.datetime.now().strftime("%Y-%m-%d")
            dats = mindate(nick, mode=1)
            if a[3] != m:
                date2 = downToThursday(date2, False)
            else:
                date2 = downToThursday(date2, True)
            if date1 >= date2:
                date1 = date2 - datetime.timedelta(days=1)
                date1 = downToThursday(date1, False)
            else:
                date1 = downToThursday(date1, False)
            # cur.execute('SELECT "Id" FROM "players" WHERE "Name" = \'%s\'' % nick)
            # plrId = cur.fetchall()[0][0]
            firstPoint = None
            impossible = False
            date1 = datetime.datetime.strftime(date1, "%Y-%m-%d")
            while firstPoint == None:
                cur.execute('SELECT "%s" FROM "walkers_killed" WHERE "player" = %s' % (date1, nick))
                firstPoint = cur.fetchall()[0][0]
                if firstPoint == None:
                    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
                    date1 = downToThursday(date1, True)
                    date1 = datetime.datetime.strftime(date1, "%Y-%m-%d")
            secondPoint = None
            date2 = datetime.datetime.strftime(date2, "%Y-%m-%d")
            while secondPoint == None:
                cur.execute('SELECT "%s" FROM "walkers_killed" WHERE "player" = %s' % (date2, nick))
                secondPoint = cur.fetchall()[0][0]
                if secondPoint == None:
                    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
                    date2 += datetime.timedelta(7)
                    date2 = datetime.datetime.strftime(date2, "%Y-%m-%d")
            ret = list()
            for base in BASELIST:
                cur.execute('SELECT "%s", "%s" FROM "%s" WHERE "player" = %s' % (date1, date2, base, nick))
                dat = cur.fetchall()
                ret.append(dat[0][1] - dat[0][0])
            ret.append(date1)
            ret.append(date2)
            ret.append(nick)
            mindat = mindate(nick)
            if date1 < mindat:
                ret = json.dumps('err')
            else:
                ret = json.dumps(ret)
    # send the respective json to requester
    resp = make_response(ret)
    resp.status_code = 200
    # two attributes below added to availability of localhost running both client and server
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.mimetype = 'application/json'
    return resp


passw = '123'
if __name__ == "__main__":
    app.run(debug=True, port=5002)