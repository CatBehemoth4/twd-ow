import datetime, confirmation
import PySimpleGUI as sg
import PIL
from PIL import ImageFilter
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askinteger
from tkcalendar import DateEntry
import tkinter.ttk as ttk
import pytesseract
from putinbase import writebase, newNick, defGroup, getnicks, BASELIST
from getpass import getpass
import os, rfr
from xlmodule import returnnicks, putinxl


class login(object):
    def __init__(self):
        self.name = ''
        self.passwd = ''


class stat(object):
    def __init__(self):
        self.id = None
        self.name = ''
        self.wk = None
        self.rd = None
        self.mp = None
        self.mc = None
        self.sf = None
        self.sc = None
        self.tph = None
        self.tpw = None
        self.cc = None
        self.sr = None
        self.l = None


def drwCap(windw):
    global labCapId, labCapNam, labCapWk, labCapRd, labCapMp, labCapMc, labCapSf, labCapSc, labCapTph, labCapTpw, labCapCc, labCapSr, labCapLvl
    labCapId = Label(windw, text='Id')
    labCapId.grid(row=5, column=0)
    labCapNam = Label(windw, text='Name')
    labCapNam.grid(row=5, column=1)
    labCapWk = Label(windw, text='Walkers killed')
    labCapWk.grid(row=5, column=2)
    labCapRd = Label(windw, text='Raiders defeated')
    labCapRd.grid(row=5, column=3)
    labCapMp = Label(windw, text='Missions played')
    labCapMp.grid(row=5, column=4)
    labCapMc = Label(windw, text='Missions completed')
    labCapMc.grid(row=5, column=5)
    labCapSf = Label(windw, text='Shots fired')
    labCapSf.grid(row=5, column=6)
    labCapSc = Label(windw, text='Stashes collected')
    labCapSc.grid(row=5, column=7)
    labCapTph = Label(windw, text='Total power heroes')
    labCapTph.grid(row=5, column=8)
    labCapTpw = Label(windw, text='Total power weapons')
    labCapTpw.grid(row=5, column=9)
    labCapCc = Label(windw, text='Cards collected')
    labCapCc.grid(row=5, column=10)
    labCapSr = Label(windw, text='Survivors rescued')
    labCapSr.grid(row=5, column=11)
    labCapLvl = Label(windw, text='Level')
    labCapLvl.grid(row=5, column=12)


def negate(img):
    for i in range(0, img.size[0] - 1):
        for j in range(0, img.size[1] - 1):
            colrs = img.getpixel((i, j))
            rpix = 255 - colrs[0]
            gpix = 255 - colrs[1]
            bpix = 255 - colrs[2]
            img.putpixel((i, j), (rpix, gpix, bpix))
    return img


def recogNumber(initBord, img):
    i = initBord[0] - 2
    j = initBord[1] - 2
    k = initBord[2] - 2
    l = initBord[3] - 2
    found = False
    while i <= initBord[0] + 6:
        while j <= initBord[1] + 6:
            while k <= initBord[2] + 6:
                while l <= initBord[3] + 6:
                    img1 = img.crop((i, j, k, l))
                    res = pytesseract.image_to_string(img1, lang='twd')
                    res = nospace(res)
                    if res != None:
                        found = True
                    if found:
                        break
                    else:
                        l += 1
                if found:
                    break
                else:
                    k += 1
            if found:
                break
            else:
                j += 1
        if found:
            break
        else:
            i += 1
    if isinstance(res, int):
        return res
    return nospace(res)



def nospace(word):
    res = ''
    if word == None:
        word = ''
    for i in range(0, len(word)):
        if word[i] != ' ':
            res = res + word[i]
    try:
        return int(res)
    except:
        return None

#
# def takeImage(x, y, img):
#
#

def unrecnumb(parm, plr, filename):
    return askinteger('Unknown digit',
                      '%s of player %s is not recognized. Enter parameter from file %s: ' % (parm, plr, filename),
                      minvalue=0)
        # int(input('%s of player %s is not recognized. Enter parameter from file %s: ' % (parm, plr, filename)))


def recognizeImages(cur, conn):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Cat Behemoth\AppData\Local\Tesseract-OCR\tesseract.exe'

# getting list of correct nicknames
#     print('You have choosen group "%s"' % (defGroup(grp, cur, conn)))
    nicksAll = getnicks(cur, conn)
    nicks = [nk[0] for nk in nicksAll]
    nams = dict()
    for nm in nicksAll:
        nams[nm[1]] = nm[0]
    # list of all images in directory
    files = os.listdir('img')
    datas = list()
    nickempty = False
    noneflag = False
    saveindex = 1
    for fname in files:
        fname = 'img' + "\\" + fname
        imagebig = PIL.Image.open(fname)
            # select fragment for stat numbers
        imagesmall = imagebig.crop((392, 297, 808, 366))
        imagesmall1 = imagebig.crop((390, 297, 678, 366))
        imagesmall2 = imagebig.crop((393, 310, 590, 357))
        imagesmall = negate(imagesmall)
        imagesmall1 = imagesmall1.filter(ImageFilter.EDGE_ENHANCE)
        imagesmall = imagesmall.filter(ImageFilter.EDGE_ENHANCE)
    # imagesmall2 = imagesmall2.filter(ImageFilter.SHARPEN)
        imagesmall2 = negate(imagesmall2)
        imagesmall2 = imagesmall2.filter(ImageFilter.EDGE_ENHANCE)
    # imagesmall1 = negate(imagesmall1)
    # imagesmall1 = imagesmall1.filter(ImageFilter.EDGE_ENHANCE)
    # select fragment for nickname
    # imagebig1 = imagebig.crop((174, 1317, 447, 2097))
    # imagebig1 = imagebig.crop((174, 1169, 447, 1953))
        x1 = 174
        y1 = 1338
        imagebig1 = imagebig.crop((x1, y1, x1 + 273, y1 + 788))
    # imagebig1 = negate(imagebig1)
    # reveal nick in image
        imagebig1.save('1.jpg')
        nickr = pytesseract.image_to_string(imagesmall, lang='rus')
        nickr = nickr[:len(nickr)-2]
        nickr1 = nickr
        nicke = pytesseract.image_to_string(imagesmall)
        nicke = nicke[:len(nicke)-2]
        nicke1 = nicke
        nickt = pytesseract.image_to_string(imagesmall, lang='twn')
        nickt = nickt[:len(nickt)-2]
        nickt1 = nickt
        nickg = pytesseract.image_to_string(imagesmall, lang='deu')
        nickg = nickg[:len(nickt)]
        nickg1 = nickg
        if nickr == 'Сержз110':
            nickr = 'Серж3110'
        if nickt[:4:] == 'Kast':
            nickt = nospace(nickt)
        if nicke[:6:] == 'Who am':
            nicke = 'Who am I'
        if nickr in nicks:
            nick = nickr
        elif nicke in nicks:
            nick = nicke
        elif nickt in nicks:
            nick = nickt
        elif nickg in nicks:
            nick = nickg
        else:
            nickr = pytesseract.image_to_string(imagesmall1, lang='rus')
            nickr = nickr[:len(nickr) - 2]
            nicke = pytesseract.image_to_string(imagesmall1)
            nicke = nicke[:len(nicke) - 2]
            nickt = pytesseract.image_to_string(imagesmall1, lang='twn')
            nickt = nickt[:len(nickt) - 2]
            if nickr in nicks:
                nick = nickr
            elif nicke in nicks:
                nick = nicke
            elif nickt in nicks:
                nick = nickt
            else:
                nickr = pytesseract.image_to_string(imagesmall2, lang='rus')
                nickr = nickr[:len(nickr)-2]
                nicke = pytesseract.image_to_string(imagesmall2)
                nicke = nicke[:len(nicke)-2]
                nickt = pytesseract.image_to_string(imagesmall2, lang='twn')
                nickt = nickt[:len(nickt)-2]
                if nickr in nicks:
                    nick = nickr
                elif nicke in nicks:
                    nick = nicke
                elif nickt in nicks:
                    nick = nickt
                else:
                    nick = ''
        if nick != '':
            allPossiblePlayers = list()
            for rec in nicksAll:
                if nick == rec[0]:
                    allPossiblePlayers.append(rec)
        imagesmall2.save('im1.jpg')

    # select fragments of stat data
        wkim = imagebig1.crop((21, 7, 260, 63))
        rdim = imagebig1.crop((21, 89, 260, 142))
        mpim = imagebig1.crop((21, 167, 260, 218))  #22 166 260 218
        mcim = imagebig1.crop((21, 244, 260, 294))  #22 244 260 294
        sfim = imagebig1.crop((21, 323, 260, 376))
        scim = imagebig1.crop((21, 396, 260, 454))
        phim = imagebig1.crop((21, 478, 260, 532))
        pwim = imagebig1.crop((21, 552, 260, 608))
        ccim = imagebig1.crop((21, 632, 260, 689))
        srim = imagebig1.crop((21, 709, 260, 764))  #28, 711, 260, 762
        lvim = imagebig.crop((289, 287, 329, 323)) #.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # rdim.save('rdim.jpg')

    # reveal stat numbers from images
        wk = pytesseract.image_to_string(wkim, lang='twd')
        wk = nospace(wk)
        if wk == None:
            wk = recogNumber((21, 7, 260, 63), imagebig1)
        if wk == None:
            wk = confirmation.sggetint(nick, fname, BASELIST[0])
        rd = pytesseract.image_to_string(rdim, lang='twd')
        rd = nospace(rd)
        if rd == None:
            rd = recogNumber((21, 89, 260, 142), imagebig1)
        if rd == None:
            rd = confirmation.sggetint(nick, fname, BASELIST[1])
        mp = pytesseract.image_to_string(mpim, lang='twd')
        mp = nospace(mp)
        if mp == None:
            mp = confirmation.sggetint(nick, fname, BASELIST[2])
        mc = pytesseract.image_to_string(mcim, lang='twd')
        mc = nospace(mc)
        if mc == None:
            mc =  recogNumber((21, 244, 260, 294), imagebig1)
        if mc == None:
            mc = confirmation.sggetint(nick, fname, BASELIST[3])
        sf = pytesseract.image_to_string(sfim, lang='twd')
        sf = nospace(sf)
        if sf == None:
            recogNumber((21, 323, 260, 376), imagebig1)
        if sf == None:
            sf = confirmation.sggetint(nick, fname, BASELIST[4])
        sc = pytesseract.image_to_string(scim, lang='twd')
        sc = nospace(sc)
        if sc == None:
            sc = recogNumber((21, 396, 260, 454), imagebig1)
        if sc == None:
            sc = confirmation.sggetint(nick, fname, BASELIST[5])
        ph = pytesseract.image_to_string(phim, lang='twd')
        ph = nospace(ph)
        if ph == None:
            ph = confirmation.sggetint(nick, fname, BASELIST[6])
        pw = pytesseract.image_to_string(pwim, lang='twd')
        pw = nospace(pw)
        if pw == None:
            pw = confirmation.sggetint(nick, fname, BASELIST[7])
        cc = pytesseract.image_to_string(ccim, lang='twd')
        cc = nospace(cc)
        if cc == None:
            cc = confirmation.sggetint(nick, fname, BASELIST[8])
        sr = pytesseract.image_to_string(srim, lang='twd')
        sr = nospace(sr)
        if sr == None:
            sr = confirmation.sggetint(nick, fname, BASELIST[9])
        try:
            lv = int(pytesseract.image_to_string(lvim))
        except:
            lv = confirmation.sggetint(nick, fname, BASELIST[10])
        datas.append([nick, wk, rd, mp, mc, sf, sc, ph, pw, cc, sr, lv, nick])
        if None in datas[len(datas) - 1]:
            noneflag = True
            break
        print(nick, wk, rd, mp, mc, sf, sc, ph, pw, cc, sr, lv)
        if nick == '':
            ncks = (nicke1, nickr1, nickt1, nickg1)
            newNck = confirmation.confsg(ncks)
            if newNck not in nicks:
                nickId = newNick(newNck, cur, conn)
                nick = newNck
                datas[len(datas) - 1][0] = nickId
                datas[len(datas) - 1][12] = nick
            else:
                for nk in nicksAll:
                    if nk[0] == newNck:
                        nick = newNck
                        datas[len(datas) - 1][0] = nk[1]
                        datas[len(datas) - 1][12] = nick
            print(nick, wk, rd, mp, mc, sf, sc, ph, pw, cc, sr, lv)
        else:
            if len(allPossiblePlayers) > 1:
                datas[len(datas) - 1][0] = confirmation.sgchooseplayer(allPossiblePlayers)
            elif len(allPossiblePlayers) == 1:
                datas[len(datas) - 1][0] = allPossiblePlayers[0][1]
    nickempty = False
    for dat in datas:
        if dat[0] == '':
            nickempty = True

# write to destination base on server if all nicks are recognized
#     if not nickempty and not noneflag:
#         writebase(datas, grp, usr, passwd)
#     elif nickempty:
#         print('There are empty unrecognized nicks in the list')
#     else:
#         print('There are unrecognized numbers in the list')

# write to destination (cards.xlsx) if all nicks are recognized
#     putinxl(datas)
    return datas, nams

# logIn = login()
# plars = list()
# parms = ['wk', 'rd', 'mp', 'mc', 'sf', 'sc', 'tph', 'tpw', 'cc', 'sr', 'l']
#
# windw = Tk()
# windw.geometry('1800x1000')
#
# def auth():
#
#     authWin = Tk()
#     authWin.title = 'Authorization'
#     authWin.geometry('350x350')
#     authWin['bg'] = 'yellow'
#     authWin.resizable(False, False)
#     user = StringVar()
#     password = StringVar()
#
#
#     def clickAuth():
#         logIn.name = nameTxt.get()
#         logIn.passwd = passwTxt.get()
#         authWin.destroy()
#
#
#     nameLabel = Label(authWin, text='Login', justify=CENTER)
#     nameLabel.pack()
#
#     nameTxt = Entry(authWin, textvariable=user)
#     nameTxt.pack()
#
#     passwLabel = Label(authWin, text='Password', justify=CENTER)
#     passwLabel.pack()
#
#     passwTxt = Entry(authWin, textvariable=password, show='*')
#     passwTxt.pack()
#
#     butAuth = Button(authWin, text='Login', command=clickAuth)
#     butAuth.pack()
#
#     authWin.mainloop()
#
#
# def recognize():
#     inputGroup['state'] = DISABLED
#     inputGroup.update()
#
#     def basePut():
#         dat = dateEntr.get_date()
#         dat = dat.strftime("%Y-%m-%d")
#         dts = list()
#         for i in range(totPl):
#             pl = list()
#             pl.append(int(globals()['LabelId' + str(i)]['text']))
#             pl.append(int(globals()['wkVar' + str(i)].get()))
#             pl.append(int(globals()['rdVar' + str(i)].get()))
#             pl.append(int(globals()['mpVar' + str(i)].get()))
#             pl.append(int(globals()['mcVar' + str(i)].get()))
#             pl.append(int(globals()['sfVar' + str(i)].get()))
#             pl.append(int(globals()['scVar' + str(i)].get()))
#             pl.append(int(globals()['tphVar' + str(i)].get()))
#             pl.append(int(globals()['tpwVar' + str(i)].get()))
#             pl.append(int(globals()['ccVar' + str(i)].get()))
#             pl.append(int(globals()['srVar' + str(i)].get()))
#             pl.append(int(globals()['lVar' + str(i)].get()))
#             pl.append(globals()['namVar' + str(i)].get())
#             dts.append(pl)
#             globals()['LabelId' + str(i)].destroy()
#             globals()['LabelName' + str(i)].destroy()
#             globals()['LabelWk' + str(i)].destroy()
#             globals()['LabelRd' + str(i)].destroy()
#             globals()['LabelMp' + str(i)].destroy()
#             globals()['LabelMc' + str(i)].destroy()
#             globals()['LabelSf' + str(i)].destroy()
#             globals()['LabelSc' + str(i)].destroy()
#             globals()['LabelTph' + str(i)].destroy()
#             globals()['LabelTpw' + str(i)].destroy()
#             globals()['LabelCc' + str(i)].destroy()
#             globals()['LabelSr' + str(i)].destroy()
#             globals()['LabelL' + str(i)].destroy()
#             dateEntr.destroy()
#             btnPutInBase.destroy()
#             inputGroup['state'] = NORMAL
#             globals()['labCapId'].destroy()
#             globals()['labCapNam'].destroy()
#             globals()['labCapWk'].destroy()
#             globals()['labCapRd'].destroy()
#             globals()['labCapMp'].destroy()
#             globals()['labCapMc'].destroy()
#             globals()['labCapSf'].destroy()
#             globals()['labCapSc'].destroy()
#             globals()['labCapTph'].destroy()
#             globals()['labCapTpw'].destroy()
#             globals()['labCapCc'].destroy()
#             globals()['labCapSr'].destroy()
#             globals()['labCapLvl'].destroy()
#         writebase(dts, grp.get(), dat, logIn.name, logIn.passwd)
#         dts.clear()
#         grpNameLabel['text'] = ''
#         grpNameLabel.update()
#         inputGroup['state'] = NORMAL
#         inputGroup.update()
#
#     gr = grp.get()
#     try:
#         gr = int(gr)
#         grNam = defGroup(gr, logIn.name, logIn.passwd)
#         grpNameLabel = Label(windw, text=grNam)
#         grpNameLabel.grid(row=1, column=5)
#         grpNameLabel.update()
#     except:
#         grNam = None
#     if not grNam:
#         messagebox.showinfo('Not exist','Group with id "' + str(gr) + '" does not exist!')
#         inputGroup['state'] = NORMAL
#         inputGroup.update()
#     else:
#         plrs, nams = recognizeImages(logIn.name, logIn.passwd, windw, gr)
#         drwCap(windw)
#         plr = stat()
#         global totPl
#         totPl = len(plrs)
#         plars.clear()
#         for i in range(len(plrs)):
#             plr.id = plrs[i][0]
#             plr.name = plrs[i][12]
#             plr.wk = plrs[i][1]
#             plr.rd = plrs[i][2]
#             plr.mp = plrs[i][3]
#             plr.mc = plrs[i][4]
#             plr.sf = plrs[i][5]
#             plr.sc = plrs[i][6]
#             plr.tph = plrs[i][7]
#             plr.tpw = plrs[i][8]
#             plr.cc = plrs[i][9]
#             plr.sr = plrs[i][10]
#             plr.l = plrs[i][11]
#             plars.append(plr)
#             labName = 'LabelId' + str(i)
#             globals()[labName] = Label(windw, text=str(plars[i].id))
#             globals()[labName].grid(row=7 + i, column=0)
#             edName = 'LabelName' + str(i)
#             namTxtVar = 'namVar' + str(i)
#             globals()[namTxtVar] = StringVar()
#             globals()[edName] = Entry(windw, textvariable=globals()[namTxtVar])
#             globals()[namTxtVar].set(plars[i].name)
#             globals()[edName].grid(row=7 + i, column=1)
#             wkName = 'LabelWk' + str(i)
#             wkTxtVar = 'wkVar' + str(i)
#             globals()[wkTxtVar] = StringVar()
#             globals()[wkName] = Entry(windw, textvariable=globals()[wkTxtVar], justify=CENTER)
#             globals()[wkTxtVar].set(plars[i].wk)
#             globals()[wkName].grid(row=7 + i, column=2)
#             rdName = 'LabelRd' + str(i)
#             rdTxtVar = 'rdVar' + str(i)
#             globals()[rdTxtVar] = StringVar()
#             globals()[rdName] = Entry(windw, textvariable=globals()[rdTxtVar], justify=CENTER)
#             globals()[rdTxtVar].set(plars[i].rd)
#             globals()[rdName].grid(row=7 + i, column=3)
#             mpName = 'LabelMp' + str(i)
#             mpTxtVar = 'mpVar' + str(i)
#             globals()[mpTxtVar] = StringVar()
#             globals()[mpName] = Entry(windw, textvariable=globals()[mpTxtVar], justify=CENTER)
#             globals()[mpTxtVar].set(plars[i].mp)
#             globals()[mpName].grid(row=7 + i, column=4)
#             mcName = 'LabelMc' + str(i)
#             mcTxtVar = 'mcVar' + str(i)
#             globals()[mcTxtVar] = StringVar()
#             globals()[mcName] = Entry(windw, textvariable=globals()[mcTxtVar], justify=CENTER)
#             globals()[mcTxtVar].set(plars[i].mc)
#             globals()[mcName].grid(row=7 + i, column=5)
#             sfName = 'LabelSf' + str(i)
#             sfTxtVar = 'sfVar' + str(i)
#             globals()[sfTxtVar] = StringVar()
#             globals()[sfName] = Entry(windw, textvariable=globals()[sfTxtVar], justify=CENTER)
#             globals()[sfTxtVar].set(plars[i].sf)
#             globals()[sfName].grid(row=7 + i, column=6)
#             scName = 'LabelSc' + str(i)
#             scTxtVar = 'scVar' + str(i)
#             globals()[scTxtVar] = StringVar()
#             globals()[scName] = Entry(windw, textvariable=globals()[scTxtVar], justify=CENTER)
#             globals()[scTxtVar].set(plars[i].sc)
#             globals()[scName].grid(row=7 + i, column=7)
#             tphName = 'LabelTph' + str(i)
#             tphTxtVar = 'tphVar' + str(i)
#             globals()[tphTxtVar] = StringVar()
#             globals()[tphName] = Entry(windw, textvariable=globals()[tphTxtVar], justify=CENTER)
#             globals()[tphTxtVar].set(plars[i].tph)
#             globals()[tphName].grid(row=7 + i, column=8)
#             tpwName = 'LabelTpw' + str(i)
#             tpwTxtVar = 'tpwVar' + str(i)
#             globals()[tpwTxtVar] = StringVar()
#             globals()[tpwName] = Entry(windw, textvariable=globals()[tpwTxtVar], justify=CENTER)
#             globals()[tpwTxtVar].set(plars[i].tpw)
#             globals()[tpwName].grid(row=7 + i, column=9)
#             ccName = 'LabelCc' + str(i)
#             ccTxtVar = 'ccVar' + str(i)
#             globals()[ccTxtVar] = StringVar()
#             globals()[ccName] = Entry(windw, textvariable=globals()[ccTxtVar], justify=CENTER)
#             globals()[ccTxtVar].set(plars[i].cc)
#             globals()[ccName].grid(row=7 + i, column=10)
#             srName = 'LabelSr' + str(i)
#             srTxtVar = 'srVar' + str(i)
#             globals()[srTxtVar] = StringVar()
#             globals()[srName] = Entry(windw, textvariable=globals()[srTxtVar], justify=CENTER)
#             globals()[srTxtVar].set(plars[i].sr)
#             globals()[srName].grid(row=7 + i, column=11)
#             lName = 'LabelL' + str(i)
#             lTxtVar = 'lVar' + str(i)
#             globals()[lTxtVar] = StringVar()
#             globals()[lName] = Entry(windw, textvariable=globals()[lTxtVar], justify=CENTER)
#             globals()[lTxtVar].set(plars[i].l)
#             globals()[lName].grid(row=7 + i, column=12)
#         # global dateEntr
#         dateEntr = DateEntry(windw)
#         dateEntr.set_date(datetime.date.today())
#         dateEntr.grid(column= 7, row= 8 + len(plrs))
#         btnPutInBase = Button(windw, text='To Base', command= basePut)
#         btnPutInBase.grid(column= 8, row= 8 + len(plrs))
#
# # frmHigh = tkinter.ttk.Frame(windw, padding= 20)
# # frmHigh.pack()
# grp = StringVar()
# buttonLog = Button(windw, text= 'Login', command= auth)
# buttonLog.grid(row=0, column=7)
# inputGroup = Entry(windw, textvariable= grp)
# labGroup = Label(windw, text='Group number')
# inputGroup.grid(row=1, column=3)
# labGroup.grid(row=1, column=0, columnspan=2)
# button = Button(windw, text= 'Input images', command= recognize)
# button.grid(row=1, column=7)
# frmShowAdds = Frame(windw, highlightbackground= 'black', highlightthickness = 2)
# frmShowAdds.grid(row=3, column=0)
# windw.mainloop()
