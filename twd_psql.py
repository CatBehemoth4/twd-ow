import psycopg2
from getpass import getpass
import datetime
from putinbase import BASELIST
import xlmodule


def baseConnect(passwd):
    connection = psycopg2.connect(dbname="TWD", user="postgres", password=passwd, host="188.120.240.167")
    cursor = connection.cursor()
    return cursor, connection


def seasonsDates(passwd):
    cursor, con = baseConnect(passwd)
    cursor.execute('SELECT * FROM "seasons" ORDER BY "Id"')
    seasonDates = cursor.fetchall()
    cursor.close()
    con.close()
    return seasonDates


def getSeasonNames(passwd):
    seasonDates = seasonsDates(passwd)
    seasonNames = tuple()
    for season in seasonDates:
        seasonNames += (season[1],)
    return seasonNames


def getSeasonDates(passwd, seasonName):
    cursor, con = baseConnect(passwd)
    cursor.execute('SELECT * FROM "seasons" WHERE "Name" = %s' % (seasonName))
    dates = cursor.fetchall()
    cursor.close()
    dates = (dates[2], dates[3], dates[4], dates[5], dates[6], dates[7], dates[8])
    cursor.close()
    con.close()
    return dates

def allWeekStat(passwd, currDat):
    cur, conn = baseConnect(passwd)
    seasonDates = seasonsDates(passwd)
    crossSeason = False
    for season in seasonDates:
        if season[3] < datetime.datetime.strptime(currDat, "%Y-%m-%d").date() < season[8]:
            neededSeason = season[1]
            crossSeason = False
            break
        elif currDat == season[2]:
            neededSeason = season[0] - 1
            crossSeason = True
            break
    if crossSeason:
        for season in seasonDates:
            if neededSeason == season[0]:
                prevDat = season[7]
    else:
        prevDat = datetime.datetime.strptime(currDat, "%Y-%m-%d").date() - datetime.timedelta(days=7)
    cur.execute('SELECT "player", "%s", "%s" FROM "walkers_killed" ORDER BY "player"' % (currDat, datetime.datetime.strftime(prevDat, "%Y-%m-%d")))
    dts = cur.fetchall()
    rw = list()
    allDats = list()
    i = 0
    for rec in dts:
        if (rec[1] != None) & (rec[2] != None):
            rw += [rec[0],]
            allDats += [rw,]
            i += 1
            rw = []
    col = 1
    for base in BASELIST:
        cur.execute('SELECT "player", "%s", "%s" FROM "%s" ORDER BY "player"' % (currDat, datetime.datetime.strftime(prevDat, "%Y-%m-%d"), base))
        dts = cur.fetchall()
        for rec in dts:
            for i in range(len(allDats)):
                if allDats[i][0] == rec[0]:
                    allDats[i] += [rec[1] - rec[2],]
                    col += 1
                    break
    cur.execute('SELECT "Id", "Name" FROM "players"')
    names = cur.fetchall()
    for i in range(len(allDats)):
        for rec in names:
            if allDats[i][0] == rec[0]:
                allDats[i][0] = rec[1]
    cur.close()
    conn.close()
    return allDats

def sortByCol(table, number):
    for i in range(1, len(table)):
        j = i - 1
        while (j >= 0) & (table[i][number] >= table[j][number]):
            j -= 1
        j += 1
        m = i
        if j != m:
            repl = table[m]
            while m != j:
                table[m] = table[m - 1]
                m -= 1
            table[m] = repl
    return table

def fillTeamOne():
    cur, conn = baseConnect(passwd)
    cur.execute('SELECT * FROM "missions_played"')
    dats = cur.fetchall()
    colNames = list()
    for desc in cur.description:
        colNames += [desc[0],]
    cur.execute('CREATE TABLE "teams" ("player" INT, FOREIGN KEY ("player") REFERENCES "players"("Id"))')
    for i in range(1, len(colNames)):
        cur.execute('ALTER TABLE "teams" ADD COLUMN "%s" INT' % (colNames[i]))
    for rec in dats:
        cur.execute('INSERT INTO "teams" ("player") VALUES (%s)' % (rec[0]))
        for i in range(1, len(rec)):
            if rec[i]:
                cur.execute('UPDATE "teams" SET "%s" = 1 WHERE "player" = %s' % (colNames[i], rec[0]))
    conn.commit()
    conn.close()

        
def groupStat():
    cur, conn = baseConnect(passwd)
    grp = int(input('Enter group Id:'))
    dat = input('Enter date:')
    dat2 = datetime.datetime.strptime(dat, '%Y-%m-%d')
    dat1 = dat2 - datetime.timedelta(days=7)
    datPrv = datetime.datetime.strftime(dat1, '%Y-%m-%d')
    cur.execute('SELECT "player" FROM "teams" WHERE "%s" = %s' % (dat, grp))
    plrs1 = cur.fetchall()
    cur.execute('SELECT "player" FROM "teams" WHERE "%s" = %s' % (datPrv, grp))
    plrs2 = cur.fetchall()
    firstSet = list()
    i = 0
    for plr in plrs1:
        plr = plr[0]
        firstSet.append([plr],)
        for base in BASELIST:
            cur.execute('SELECT "%s" FROM "%s" WHERE "player" = %s' % (dat, base, plr))
            bz = cur.fetchall()
            bz1 = bz[0][0]
            firstSet[i].append(bz1)
        i += 1
    secondSet = list()
    i = 0
    for plr in plrs2:
        plr = plr[0]
        secondSet.append([plr],)
        for base in BASELIST:
            cur.execute('SELECT "%s" FROM "%s" WHERE "player" = %s' % (datPrv, base, plr))
            bz = cur.fetchall()
            bz1 = bz[0][0]
            secondSet[i].append(bz1)
        i += 1
    reslt = list()
    j = 0
    for set1 in firstSet:
        for set2 in secondSet:
            if set1[0] == set2[0]:
                reslt.append([set1[0]])
                for i in range(1, len(set1)):
                    reslt[j].append(set1[i] - set2[i])
                j += 1
    finReslt = list()
    while len(reslt) > 0:
        line = 0
        indOfMax = 0
        max = reslt[line][4]
        while line < len(reslt) - 1:
            line += 1
            if reslt[line][4] > max:
                indOfMax = line
                max = reslt[line][4]
        finReslt.append(reslt[indOfMax])
        reslt.pop(indOfMax)
    for i in range(len(finReslt)):
        cur.execute('SELECT "Name" FROM "players" WHERE "Id" = %s' % (finReslt[i][0]))
        nam = cur.fetchall()
        nam = nam[0][0]
        finReslt[i][0] = nam
    for lin in finReslt:
        print(lin)
    try:
        q = int(input('Export to excel? Enter "1" for yes.'))
        if q == 1:
            xlmodule.putinxlext(finReslt)
    except:
        pass

    cur.close()
    conn.close()

            



passwd = getpass("Enter password:")
groupStat()

# allDats = allWeekStat(passwd, '2020-06-18')
# allDats = sortByCol(allDats, 4)
# maxes = list()
# for i in range (1, len(allDats[0]) - 1):
#     maxes += [allDats[0][i],]
#     for j in range(1, len(allDats)):
#         if allDats[j][i] > maxes[i - 1]:
#             maxes[i - 1] = allDats[j][i]


# # for rebuilding base
# cursor, con = baseConnect(passwd)
# dats = tuple()
# for i in range(1, 41):
#
# # reading all player's stats
#     if (i != 31):
#         req = 'SELECT * from "zplayer%s" ORDER BY "dt"' % (i)
#         cursor.execute(req)
#         print('Player ' + str(i) + ' found')
#         player = cursor.fetchall()
# # getting list of dates
#         if i == 1:
#             for line in player:
#                 dats += (line[0],)
#
# # defining starting column
#         for m in range(len(player)):
#             if m == 0:
#                 j = 0
#                 while j < len(dats) - 1:
#                     if dats[j] <= player[0][0] < dats[j + 1]:
#                         colind = j
#                     j += 1
#
#         if i != 0:
#             for k in range(len(player)):
#                 req = 'UPDATE "walkers_killed" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][1], i)
#                 cursor.execute(req)
#                 cursor.execute('UPDATE "raiders_defeated" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][2], i))
#                 cursor.execute('UPDATE "missions_played" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][3], i))
#                 cursor.execute('UPDATE "missions_completed" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][4], i))
#                 cursor.execute('UPDATE "shots_fired" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][5], i))
#                 cursor.execute('UPDATE "stash_collected" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][6], i))
#                 cursor.execute('UPDATE "total_power_heroes" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][7], i))
#                 cursor.execute('UPDATE "total_power_weapons" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][8], i))
#                 cursor.execute('UPDATE "cards_collected" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][9], i))
#                 cursor.execute('UPDATE "survivors_rescued" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][10], i))
#                 cursor.execute('UPDATE "level" SET "%s" = %s WHERE "player" = %s' % (dats[colind], player[k][11], i))
#                 colind += 1
#                 con.commit()
#     else:
#         cursor.execute('DELETE FROM "walkers_killed" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "raiders_defeated" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "missions_played" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "missions_completed" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "shots_fired" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "stash_collected" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "total_power_heroes" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "total_power_weapons" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "cards_collected" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "survivors_rescued" WHERE "player" = 31')
#         cursor.execute('DELETE FROM "level" WHERE "player" = 31')
#
# cursor.close()
# con.close()


