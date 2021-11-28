import psycopg2
from getpass import getpass
import datetime
from putinbase import baseconnect, BASELIST, delPlr


def justNonone(days, values):
    res = list()
    values = list(values[0])
    for i in range(len(days)):
        if values[i+1]:
            res.append(days[i])
    return res


def similarPlayer(usr):
    passwd = getpass('Enter password for "%s":' % usr)
    cur, conn = baseconnect(usr, passwd)
    cur.execute('SELECT "Id" FROM "players"')
    plrsId = cur.fetchall()
    for i in range(len(plrsId)):
        plrsId[i] = plrsId[i][0]
    plrsIdWk = list(plrsId)
    plrcnt = 0
    casecnt = 0
    for plr1 in plrsId:
        print('Checking player # %s' % plr1)
        plrsIdWk.pop(plrsIdWk.index(plr1))
        cur.execute('SELECT * FROM "teams" WHERE "player" = %s' % plr1)
        valuesOne = cur.fetchall()
        daysOne = [desc[0] for desc in cur.description]
        daysOne.pop(0)
        if len(valuesOne) != 0:
            daysOne = justNonone(daysOne, valuesOne)
            for plr2 in plrsIdWk:
                cur.execute('SELECT * FROM "teams" WHERE "player" = %s' % plr2)
                valuesTwo = cur.fetchall()
                daysTwo = [desc[0] for desc in cur.description]
                daysTwo.pop(0)
                if len(valuesTwo) != 0:
                    daysTwo = justNonone(daysTwo, valuesTwo)
                    if set(daysOne).isdisjoint(daysTwo):
                        casecnt += 1
                        daysOne.sort()
                        daysTwo.sort()
                        if daysOne[0] > daysTwo[0]:
                            reserv = daysOne
                            daysOne = daysTwo
                            daysTwo = reserv
                            reserv = plr1
                            plr1 = plr2
                            plr2 = reserv
                        flag = False
                        for i1 in range(len(daysOne)):
                            if daysTwo[0] > daysOne[i1]:
                                i2 = i1 - 1
                                flag = True
                                break
                        if not flag:
                            i2 = len(daysOne) - 1
                        comp = [daysOne[i2], daysTwo[0]]
                        dt1 = datetime.datetime.strptime(comp[0], "%Y-%m-%d")
                        dt2 = datetime.datetime.strptime(comp[1], "%Y-%m-%d")
                        cur.execute('SELECT "%s" FROM "walkers_killed" WHERE "player" = %s' % (comp[0], plr1))
                        fk = cur.fetchall()[0][0]
                        cur.execute('SELECT "%s" FROM "walkers_killed" WHERE "player" = %s' % (comp[1], plr2))
                        sk = cur.fetchall()[0][0]
                        dt = dt1 - dt2
                        days = dt.days
                        toCheck = False
                        if 0 <= sk - fk <= days * 17000:
                            toCheck = True
                            for base in BASELIST:
                                cur.execute('SELECT "%s", "%s" FROM "%s" WHERE "player" = %s OR "player" = %s' % (
                                    comp[0], comp[1], base, plr1, plr2
                                ))
                                res = cur.fetchall()
                                try:
                                    if res[1][1] < res[0][0]:
                                        toCheck = False
                                        break
                                except:
                                    print(plr1, plr2)
                                    raise(TypeError)
                        if toCheck:
                            print('Player # %s may be the same as player # %s' % (plr1, plr2))
        print('Player # %s is checked' % plr1)
        print('%s cases' % casecnt)
        plrcnt += 1
    print('%s players checked.' % plrcnt)
    print('Total %s cases' % casecnt)


def similarPlayer1(usr):
    passwd = getpass('Enter password for %s: ' % usr)
    cur, conn = baseconnect(usr, passwd)
    cur.execute('SELECT * FROM "missions_completed"')
    teams = cur.fetchall()
    cnames = [desc[0] for desc in cur.description]
    print(cnames)
    print(teams)
    counter = 0
    for i in range(len(teams) - 1):
        plr1Chk = teams[i]
        for j in range(teams.index(plr1Chk) + 1, len(teams)):
            plr2Chk = teams[j]
            flag = True
            for k in range(1, len(plr1Chk)):
                if plr1Chk[k] and plr2Chk[k]:
                    flag = False
                    break
            if flag:
                flag1 = True
                flag2 = True
                for k in range(1, len(plr1Chk)):
                    if plr1Chk[k] and flag1:
                        idx1 = k
                        flag1 = False
                    if plr2Chk[k] and flag2:
                        idx2 = k
                        flag2 = False
                    if not flag1 and not flag2:
                        break
                if idx1 < idx2:
                    early = plr1Chk
                    late = plr2Chk
                    cnt = idx2
                else:
                    early = plr2Chk
                    late = plr1Chk
                    cnt = idx1
                k = cnt
                while not early[k]:
                    k -= 1
                datE = cnames[k]
                datL = cnames[cnt]
                datE1 = datetime.datetime.strptime(datE, "%Y-%m-%d")
                datL1 = datetime.datetime.strptime(datL, "%Y-%m-%d")
                days = (datL1 - datE1).days
                multipl = 1500
                try:
                    if early[k-1]:
                        multipl = (early[k] - early[k-1]) % 7 * 3
                except:
                    pass
                if multipl > early[k]:
                    multipl = early[k] % 2
                if (0 <= late[cnt] - early[k] < days * multipl) & (late[cnt] / early[k] < 1.4):
                    tochk = True
                    for base in BASELIST:
                        cur.execute('SELECT "%s" FROM "%s" WHERE "player" = %s' % (datL, base, late[0]))
                        second = cur.fetchall()[0][0]
                        cur.execute('SELECT "%s" FROM "%s" WHERE "player" = %s' % (datE, base, early[0]))
                        first = cur.fetchall()[0][0]
                        if second - first < 0:
                            tochk = False
                            break
                    if tochk:
                        print('Players %s and %s are potentially may be the same' % (early[0], late[0]))
                    counter += 1
    print('Total %s cases' % counter)


def mergePlayer(pl1, pl2, usr):
    passwd = getpass('Enter password for "%s":' % usr)
    cur, conn = baseconnect(usr, passwd)
    flagchoise = True
    contin = True
    while flagchoise:
        choise = input("You want to merge players %s and %s. Enter 'y' to continue or 'n' to cancel.\n" % (pl1, pl2))
        if choise == 'y':
            flagchoise = False
        if choise == 'n':
            flagchoise = False
            contin = False
    if contin:
        cur.execute('SELECT * FROM "teams" WHERE "player" = %s' % (pl1))
        dats = [i[0] for i in cur.description]
        dats.pop(0)
        teams1 = cur.fetchall()
        cur.execute('SELECT * FROM "teams" WHERE "player" = %s' % (pl2))
        teams2 = cur.fetchall()
        teams = list()
        teams.append(teams1[0])
        teams.append(teams2[0])
        print(dats, teams)
        print(len(dats), len(teams[0]))
        toBase = list()
        flag = False
        for i in range(1, len(teams[0])):
            if (teams[0][i] != None) & (teams[1][i] != None):
                flag = True
                break
            elif teams[0][i] != None:
                toBase.append(teams[0][i])
            elif teams[1][i] != None:
                toBase.append(teams[1][i])
            else:
                toBase.append(None)
        if flag:
            print('Players have shared same date results. Unable to merge them.')
            cur.close()
            conn.close()
        else:
            flag1 = False
            while not flag1:
                try:
                    res = int(input('Enter 1 to record merge into player %s or 2 - to player %s:\n' % (pl1, pl2)))
                    if res == 1 or res == 2:
                        flag1 = True
                    else:
                        print('Incorrect input, try again.')
                except:
                    print('Incorrect input, try again.')
            if res == 1:
                res = pl1
                rem = pl2
            else:
                res = pl2
                rem = pl1
            print('Updating player %s' % (res))
            print(toBase)
            if len(dats) == len(toBase):
                recordBasePlayer(res, dats, toBase, 'teams', cur, conn)
            for base in BASELIST:
                cur.execute('SELECT * FROM "%s" WHERE "player" = %s' % (base, pl1))
                dats = [i[0] for i in cur.description]
                dats.pop(0)
                datas1 = cur.fetchall()
                cur.execute('SELECT * FROM "%s" WHERE "player" = %s' % (base, pl2))
                datas2 = cur.fetchall()
                datas = list()
                datas.append(datas1[0])
                datas.append(datas2[0])
                toBase = makeRecord(datas)
                if len(dats) == len(toBase):
                    recordBasePlayer(res, dats, toBase, base, cur, conn)
            delPlr(rem, usr, passwd)
            conn.commit()
            conn.close()
            print('Players %s an %s have been merged.' % (pl1, pl2))


def recordBasePlayer(player, dates, data, base, cur, conn):
    cur, conn = cur, conn
    for i in range(len(data)):
        if data[i] != None:
            cur.execute('UPDATE "%s" SET "%s" = %s WHERE "player" = %s' % (base, dates[i], data[i], player))
        else:
            cur.execute('UPDATE "%s" SET "%s" = NULL WHERE "player" = %s' % (base, dates[i], player))
        conn.commit()
    print('Base "%s" updated' % (base))


def makeRecord(datas):
    toBase = list()
    for i in range(1, len(datas[0])):
        if datas[0][i] != None:
            toBase.append(datas[0][i])
        elif datas[1][i] != None:
            toBase.append(datas[1][i])
        else:
            toBase.append(None)
    return toBase

