import tkinter, confirmation

import psycopg2
from tkinter import messagebox
from getpass import getpass
import datetime
BASELIST = ('walkers_killed', 'raiders_defeated', 'missions_played', 'missions_completed', 'shots_fired',
            'stash_collected', 'total_power_heroes', 'total_power_weapons', 'cards_collected',
            'survivors_rescued', 'level')


global flag


def baseconnect(usr, passwd):
    connection = psycopg2.connect(dbname="TWD", user=usr, password=passwd, host="188.120.240.167", port=17344)
    cursor = connection.cursor()
    return cursor, connection


def grouplist(cur, conn, mode=0):
    cur.execute('SELECT * FROM "Groups"')
    reslt = cur.fetchall()
    if mode == 0:
        return reslt
    elif mode == 1:
        res = list()
        for row in reslt:
            res.append(str(row[0]) + ' ' + row[1])
        return res
    elif mode == 3:
        res = dict()
        for row in reslt:
            res[row[1]] = row[0]
        return res
    res = list()
    for row in reslt:
        res.append(row[1])
    return res


def datmonthcheck(day, month, year):
    if month in {2, 4, 6, 9, 11}:
        if day == 31:
            return False
    if month == 2:
        if day == 30:
            return False
        else:
            if day == 29:
                if (year % 4 != 0) & ((year % 100 == 0) & (year % 400 != 0)):
                    return False
    return True


def chkdt(dat):
    numbs = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    mnth = {'10', '01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12'}
    if dat[:2] != '20':
        return False
    if (dat[2] != '2') & (dat[3] != '3'):
        return False
    if dat[3] not in numbs:
        return False
    if (dat[4] != '-') | (dat[7] != '-'):
        return False
    if dat[5:7] not in mnth:
        return False
    try:
        dtn = int(dat[8:10])
    except:
        return False
    if not (0 < dtn < 32):
        return False
    return datmonthcheck(int(dat[8:10]), int(dat[5:7]), int(dat[:4]))


def getnicks(cursor, connection):
    cursor.execute('SELECT "Name", "Id" FROM "players"')
    intmd = cursor.fetchall()
    nicks = list()
    for rec in intmd:
        rec = [rec[0], rec[1]]
        nicks.append(rec)
    return nicks



def writebase(datas, grp, dat, cursor, connection):

    # add fields for current date to table
    for base in BASELIST:
        cursor.execute('ALTER TABLE "%s" ADD COLUMN IF NOT EXISTS "%s" INT' % (base, dat))
    cursor.execute('ALTER TABLE "teams" ADD COLUMN IF NOT EXISTS "%s" INT' % (dat))
    connection.commit()
    print('Day %s added to the table:' % (dat))

    # iterating by users in block and change nicks to playersID
    for i in range(len(datas)):
        # cursor.execute("""SELECT "Id" from "players" where "Name"='""" + datas[i][0] + "'")
        # Ids = cursor.fetchall()
        # id = Ids[0][0]

# if new player - add him into tables
        req = 'SELECT * FROM "walkers_killed" WHERE "player" = %s' % (datas[i][0])
        cursor.execute(req)
        isExist = cursor.fetchall()
        if not isExist:
            for base in BASELIST:
                cursor.execute('INSERT INTO "%s" ("player") VALUES (%s)' % (base, datas[i][0]))
            cursor.execute('INSERT INTO "teams" ("player") VALUES (%s)' % datas[i][0])

# update values in tables
        j = 1
        for base in BASELIST:
            cursor.execute('UPDATE "%s" SET "%s" = %s WHERE "player" = %s' % (base, dat, datas[i][j], datas[i][0]))
            j += 1
        cursor.execute('UPDATE "teams" SET "%s" = %s WHERE "player" = %s' % (dat, grp, datas[i][0]))
        print('Player %s (%s) updated.' % (datas[i][12], datas[i][0]))
    flag = messagebox.askyesno(title='Confirm?', message='Are you sure want to update the base?')
    if flag:
        connection.commit()
        print('commited')
    else:
        print('rejected')


def datemove(passwd):
    cursor, connection = baseconnect('postgres', passwd)
    good = False

# input dates

    while not good:
        olddate = input('Enter target date in format "YYYY-MM-DD": ')
        newdate = input('Enter destination date in format "YYYY-MM-DD": ')
        if (not chkdt(olddate)) | (not chkdt(newdate)):
            print('Incorrect date entered. Try again.')
        else:
            good = True

# replacing data in statistic tables

    for base in BASELIST:
        cursor.execute('SELECT "player", "%s" FROM "%s"' % (olddate, base))
        dats = cursor.fetchall()
        for i in range(len(dats)):
            if dats [i][1] != None:
                cursor.execute ('UPDATE "%s" SET "%s" = %s WHERE "player" = %s' % (base, newdate, dats[i][1], dats[i][0]))
        cursor.execute('ALTER TABLE "%s" DROP COLUMN "%s"' % (base, olddate))
        connection.commit()  # recording data into table

# replace data in teams table

    cursor.execute('SELECT "player", "%s" FROM "teams"' % olddate)
    dats = cursor.fetchall()
    for i in range(len(dats)):
        if dats [i][1] != None:
            cursor.execute('UPDATE "teams" SET "%s" = %s WHERE "player" = %s' % (newdate, dats[i][1], dats[i][0]))
    cursor.execute ('ALTER TABLE "teams" DROP COLUMN "%s"' % olddate)

# recording data into database and finish

    connection.commit()
    cursor.close()
    connection.close()


def deletecolumn(passwd):
    cursor, connection = baseconnect('postgres', passwd)
    deldate = input('Enter date to exclude in format "YYYY-MM-DD": ')

    for base in BASELIST:
        cursor.execute('ALTER TABLE "%s" DROP COLUMN "%s"' % (base, deldate))
    cursor.execute('ALTER TABLE "teams" DROP COLUMN "%s"' % deldate)
    connection.commit()
    cursor.close()
    connection.close()


def newNick(nick, cursor, connection):
    cursor.execute('SELECT "Id" FROM "players"')
    numbers = cursor.fetchall()
    numbers = [num[0] for num in numbers]
    numbers.sort(key= lambda x: x, reverse=True)
    nickId = numbers[0] + 1
    cursor.execute('INSERT INTO "players" ("Id", "Name") VALUES (%s, \'%s\')' % (nickId, nick))
    connection.commit()
    return nickId


def delPlr(nick, usr, passwd):
    cursor, connection = baseconnect(usr, passwd)
    cursor.execute('SELECT * FROM "players"')
    plrs = cursor.fetchall()
    found = False
    for player in plrs:
        if player[0] == nick:
            plrId = player[0]
            nm = player [1]
            found = True
            break
    if not found:
        print('Player \'%s\' is not found in base.' % nick)
    else:
        for base in BASELIST:
            cursor.execute('DELETE FROM "%s" WHERE "player" = %s' % (base, plrId))
        cursor.execute('DELETE FROM "teams" WHERE "player" = %s' % plrId)
        cursor.execute('DELETE FROM "players" WHERE "Id" = %s' % plrId)
        q = input('Are you sure want to remove \'%s\' (%s) from base. It cannot de undone?' % (nm, plrId))
        if q == 'y':
            connection.commit()
            print('Player \'%s\' has been removed from base.' % nm)
    connection.close()


def defGroup(number, cur, conn):
    try:
        cur.execute('SELECT "Name" FROM "Groups" WHERE "Id" = %s' % (number))
        result = cur.fetchall()[0][0]
    except:
        result = None
    return result
