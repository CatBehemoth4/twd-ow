from PIL import Image, ImageFilter
import pytesseract
from tkinter import *

from xlmodule import returnnicks, putinxl
from putinbase import writebase, getnicks, newNick, defGroup
from getpass import getpass
import os

class login(object):
    def __init__(self):
        self.name = ''
        self.passwd = ''


def negate(img):
    for i in range(0, img.size[0] - 1):
        for j in range(0, img.size[1] - 1):
            colrs = img.getpixel((i, j))
            rpix = 255 - colrs[0]
            gpix = 255 - colrs[1]
            bpix = 255 - colrs[2]
            img.putpixel((i, j), (rpix, gpix, bpix))
    return img


def nospace(word):
    res = ''
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
        return int(input('%s of player %s is not recognized. Enter parameter from file %s: ' % (parm, plr, filename)))

def recognizeImages(logIn):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Cat Behemoth\AppData\Local\Tesseract-OCR\tesseract.exe'

    usr = logIn.name
    passwd = logIn.passwd
    print(usr, passwd)
    print(usr, passwd)
    grp = int(input('Enter group number:'))
# enter password for root user

# getting list of correct nicknames
    print('You have choosen group "%s"' % (defGroup(grp, usr, passwd)))
    nicksAll = getnicks(usr, passwd)
    nicks = [nk[0] for nk in nicksAll]
    # list of all images in directory
    files = os.listdir('img')
    datas = list()
    nickempty = False
    noneflag = False
    saveindex = 1
    for fname in files:
        fname = 'd:\\pythonprojects\\rfr2-0\\img' + "\\" + fname
        imagebig = Image.open(fname)
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
            wk = unrecnumb('"Walkers killed"', nick, fname)
        rd = pytesseract.image_to_string(rdim, lang='twd')
        rd = nospace(rd)
        if rd == None:
            rd = unrecnumb('"Raiders defeated"', nick, fname)
        mp = pytesseract.image_to_string(mpim, lang='twd')
        mp = nospace(mp)
        if mp == None:
            mp = unrecnumb('"Missions played"', nick, fname)
        mc = pytesseract.image_to_string(mcim, lang='twd')
        mc = nospace(mc)
        if mc == None:
            mc = unrecnumb('"Missions completed"', nick, fname)
        sf = pytesseract.image_to_string(sfim, lang='twd')
        sf = nospace(sf)
        if sf == None:
            sf = unrecnumb('"Shots fired"', nick, fname)
        sc = pytesseract.image_to_string(scim, lang='twd')
        sc = nospace(sc)
        if sc == None:
            sc = unrecnumb('"Stashes collected"', nick, fname)
        ph = pytesseract.image_to_string(phim, lang='twd')
        ph = nospace(ph)
        if ph == None:
            ph = unrecnumb('"Total power heroes"', nick, fname)
        pw = pytesseract.image_to_string(pwim, lang='twd')
        pw = nospace(pw)
        if pw == None:
            pw = unrecnumb('"Total power weapons"', nick, fname)
            pwim.save('pw.jpg')
        cc = pytesseract.image_to_string(ccim, lang='twd')
        cc = nospace(cc)
        if cc == None:
            cc = unrecnumb('"Cards collected"', nick, fname)
        sr = pytesseract.image_to_string(srim, lang='twd')
        sr = nospace(sr)
        if sr == None:
            sr = unrecnumb('"Survivors rescued"', nick, fname)
        try:
            lv = int(pytesseract.image_to_string(lvim))
        except:
            lv = unrecnumb('"Level"', nick, fname)
        datas.append([nick, wk, rd, mp, mc, sf, sc, ph, pw, cc, sr, lv, nick])
        if None in datas[len(datas) - 1]:
            noneflag = True
            break
        print(nick, wk, rd, mp, mc, sf, sc, ph, pw, cc, sr, lv)
        if nick == '':
            print('Nick is not recognized as existed.')
            print('Recognized variants are: %s, %s, %s, %s.' % (nicke1, nickr1, nickt1, nickg1))
            newNck = input('Enter respective number, 0 for none or 5 for manual add: ')
            ncks = (nicke1, nickr1, nickt1, nickg1)
            if (newNck != '0') & (newNck != '5'):
                newNck = ncks[int(newNck) - 1]
            elif newNck == '5':
                newNck = input('Enter nick to add: ')
            elif newNck == '0':
                nickempty = True
            if newNck not in nicks:
                nickId = newNick(newNck, usr, passwd)
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
                print('More than one such nickname were found in base.')
                for rec in allPossiblePlayers:
                    print('%s, number %s' % (rec[0], rec[1]))
                choise = int(input('Enter correct number of variant to pick:'))
                datas[len(datas) - 1][0] = allPossiblePlayers[choise - 1][1]
            elif len(allPossiblePlayers) == 1:
                datas[len(datas) - 1][0] = allPossiblePlayers[0][1]
    nickempty = False
    for dat in datas:
        if dat[0] == '':
            nickempty = True

# write to destination base on server if all nicks are recognized
    if not nickempty and not noneflag:
        writebase(datas, grp, usr, passwd)
    elif nickempty:
        print('There are empty unrecognized nicks in the list')
    else:
        print('There are unrecognized numbers in the list')

# write to destination (cards.xlsx) if all nicks are recognized
# if not nickempty and not noneflag:
#     putinxl(datas)