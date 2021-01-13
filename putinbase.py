import psycopg2
from getpass import getpass
import datetime
BASELIST = ('walkers_killed', 'raiders_defeated', 'missions_played', 'missions_completed', 'shots_fired',
            'stash_collected', 'total_power_heroes', 'total_power_weapons', 'cards_collected',
            'survivors_rescued', 'level')


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


def getnicks(passwd):
    connection = psycopg2.connect(dbname="TWD", user="postgres", password=passwd, host="188.120.240.167")
    cursor = connection.cursor()
    cursor.execute('SELECT "Name" FROM "players"')
    intmd = cursor.fetchall()
    nicks = list()
    for rec in intmd:
        nicks.append(rec[0])
    return nicks


def writebase(datas, grp, passwd):
    # connect to base
    # passwd = getpass("Enter password:", )
    connection = psycopg2.connect(dbname="TWD", user="postgres", password=passwd, host="188.120.240.167")
    cursor = connection.cursor()
    i = input('Enter "1" for current date or "2" for custom: ')
    # getting current date
    flg = True
    while flg:
        if i == '1':
            nowmoment = datetime.datetime.today()
            dat = nowmoment.strftime("%Y-%m-%d")
            flg = False
        elif i == '2':
            flg1 = False
            while not flg1:
                dat = input('Enter date in format "YYYY-MM-DD": ')
                flg1 = chkdt(dat)
                if not flg1:
                    print('Incorrect Date, try  again.')
            flg = False
        else:
            print('Incorrect input. "1" or "2" needed.')

    # add fields for current date to table
    for base in BASELIST:
        cursor.execute('ALTER TABLE "%s" ADD COLUMN IF NOT EXISTS "%s" INT' % (base, dat))
    cursor.execute('ALTER TABLE "teams" ADD COLUMN IF NOT EXISTS "%s" INT' % (dat))
    connection.commit()
    print('Day %s added to the table:' % (dat))

    # iterating by users in block and change nicks to playersID
    for i in range(len(datas)):
        cursor.execute("""SELECT "Id", "Group" from "players" where "Name"='""" + datas[i][0] + "'")
        Ids = cursor.fetchall()
        id = Ids[0][0]

# if new player - add him into tables
        req = 'SELECT * FROM "walkers_killed" WHERE "player" = %s' % (id)
        cursor.execute(req)
        isExist = cursor.fetchall()
        if not isExist:
            for base in BASELIST:
                cursor.execute('INSERT INTO "%s" ("player") VALUES (%s)' % (base, id))
            cursor.execute('INSERT INTO "teams" ("player") VALUES (%s)' % id)

# update values in tables
        j = 1
        for base in BASELIST:
            cursor.execute('UPDATE "%s" SET "%s" = %s WHERE "player" = %s' % (base, dat, datas[i][j], id))
            j += 1
        cursor.execute('UPDATE "teams" SET "%s" = %s WHERE "player" = %s' % (dat, grp, id))
        print('Player %s (%s) updated.' % (datas[i][0], id))
    n = int(input('Enter "1" to confirm recording:'))
    if n == 1:
        connection.commit()
    cursor.close()
    connection.close()


def datemove():
    passwd = getpass("Enter password:", )
    connection = psycopg2.connect(dbname="TWD", user="postgres", password=passwd, host="188.120.240.167")
    cursor = connection.cursor()
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


def deletecolumn():

    passwd = getpass("Enter password:", )
    connection = psycopg2.connect(dbname="TWD", user="postgres", password=passwd, host="188.120.240.167")
    cursor = connection.cursor()
    deldate = input('Enter date to exclude in format "YYYY-MM-DD": ')

    for base in BASELIST:
        cursor.execute('ALTER TABLE "%s" DROP COLUMN "%s"' % (base, deldate))
    cursor.execute('ALTER TABLE "teams" DROP COLUMN "%s"' % deldate)
    connection.commit()
    cursor.close()
    connection.close()