import psycopg2
from getpass import getpass
import datetime
BASELIST = ('walkers_killed', 'raiders_defeated', 'missions_played', 'missions_completed', 'shots_fired',
            'stash_collected', 'total_power_heroes', 'total_power_weapons', 'cards_collected',
            'survivors_rescued', 'level')

def baseconnect(passwd):
    connection = psycopg2.connect(dbname="TWD", user="postgres", password=passwd, host="188.120.240.167")
    cursor = connection.cursor()
    return cursor, connection



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
    cursor, connection = baseconnect(passwd)
    cursor.execute('SELECT "Name", "Id" FROM "players"')
    intmd = cursor.fetchall()
    nicks = list()
    for rec in intmd:
        rec = [rec[0], rec[1]]
        nicks.append(rec)
    return nicks


def writebase(datas, grp, passwd):
    # connect to base
    # passwd = getpass("Enter password:", )
    cursor, connection = baseconnect(passwd)
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
    n = int(input('Enter "1" to confirm recording:'))
    if n == 1:
        connection.commit()
    cursor.close()
    connection.close()


def datemove(passwd):
    cursor, connection = baseconnect(passwd)
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
    cursor, connection = baseconnect(passwd)
    deldate = input('Enter date to exclude in format "YYYY-MM-DD": ')

    for base in BASELIST:
        cursor.execute('ALTER TABLE "%s" DROP COLUMN "%s"' % (base, deldate))
    cursor.execute('ALTER TABLE "teams" DROP COLUMN "%s"' % deldate)
    connection.commit()
    cursor.close()
    connection.close()


def newNick(nick, passwd):
    cursor, connection = baseconnect(passwd)
    cursor.execute('SELECT "Id" FROM "players"')
    numbers = cursor.fetchall()
    numbers = [num[0] for num in numbers]
    numbers.sort(key= lambda x: x, reverse=True)
    nickId = numbers[0] + 1
    cursor.execute('INSERT INTO "players" ("Id", "Name") VALUES (%s, \'%s\')' % (nickId, nick))
    connection.commit()
    connection.close()
    return nickId


def delNick(nick, passwd):
    cursor, connection = baseconnect(passwd)
    cursor.execute('SELECT * FROM "players"')
    plrs = cursor.fetchall()
    found = False
    for player in plrs:
        if player[1] == nick:
            plrId = player[0]
            found = True
            break
    if not found:
        print('Player \'%s\' is not found in base.' % nick)
    else:
        for base in BASELIST:
            cursor.execute('DELETE FROM "%s" WHERE "player" = %s' % (base, plrId))
        cursor.execute('DELETE FROM "teams" WHERE "player" = %s' % plrId)
        cursor.execute('DELETE FROM "players" WHERE "Id" = %s' % plrId)
        q = input('Are you sure want to remove \'%s\' (%s) from base. It cannot de undone?' % (nick, plrId))
        if q == 'y':
            connection.commit()
            print('Player \'%s\' has been removed from base.' % nick)
    connection.close()
