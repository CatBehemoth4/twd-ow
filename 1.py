from PIL import Image, ImageFilter
import pytesseract
from xlmodule import returnnicks, putinxl
from putinbase import writebase, getnicks
from getpass import getpass
import os


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


def unrecnumb(parm, plr, filename):
        return int(input('%s of player %s is not recognized. Enter parameter from file %s: ' % (parm, plr, filename)))


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Cat Behemoth\AppData\Local\Tesseract-OCR\tesseract.exe'

grp = int(input('Enter group number:'))

# enter password for root user
passwd = getpass('Enter password: ')
# getting list of correct nicknames
nicks = getnicks(passwd)
# list of all images in directory
files = os.listdir('img')
datas = list()
nickempty = False
noneflag = False
saveindex = 1
for fname in files:
    fname = 'img' + "\\" + fname
    imagebig = Image.open(fname)
    # select fragment for stat numbers
    imagesmall = imagebig.crop((390, 297, 808, 366))
    imagesmall1 = imagebig.crop((390, 297, 678, 366))
    imagesmall2 = imagesmall
    imagesmall = negate(imagesmall)
    imagesmall1 = imagesmall1.filter(ImageFilter.EDGE_ENHANCE)
    imagesmall = imagesmall.filter(ImageFilter.EDGE_ENHANCE)
    # imagesmall1 = negate(imagesmall1)
    # imagesmall1 = imagesmall1.filter(ImageFilter.EDGE_ENHANCE)
    # select fragment for nickname
    imagebig1 = imagebig.crop((174, 1317, 447, 2097))
    #imagebig1 = negate(imagebig1)
    # reveal nick in image
    nickr = pytesseract.image_to_string(imagesmall, lang='rus')
    nickr = nickr[:len(nickr)-2]
    nicke = pytesseract.image_to_string(imagesmall)
    nicke = nicke[:len(nicke)-2]
    nickt = pytesseract.image_to_string(imagesmall, lang='twn')
    nickt = nickt[:len(nickt)-2]
    nickg = pytesseract.image_to_string(imagesmall, lang='deu')
    nickg = nickg[:len(nickt)]
    if nickr == 'Сержз110':
        nickr = 'Серж3110'
    if nickt[:4:] == 'Kast':
        nickt = nospace(nickt)
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

    # if nick[-5::] == ' EDIT' or nick[-5::] == ' EDlт':
    #     nick = nick[:-5:]
    # if nick[:2:] == 'ma':
    #     nick = 'Ooo'
    # nickq = input('Current nick is ' + nick + '. Enter correct nick or hit "enter" to unchange')
    # if nickq != '':
    #     nick = nickq

    # select fragments of stat data
    wkim = imagebig1.crop((22, 7, 260, 63))
    rdim = imagebig1.crop((28, 89, 260, 142))
    rdim1 = imagebig1.crop((22, 89, 260, 142))
    mpim = imagebig1.crop((22, 166, 260, 218))  #22 166 260 218
    mcim = imagebig1.crop((22, 244, 260, 294))  #22 244 260 294
    sfim = imagebig1.crop((22, 323, 260, 376))
    scim = imagebig1.crop((28, 396, 260, 454))
    scim1 = imagebig1.crop((20, 390, 260, 458))
    phim = imagebig1.crop((22, 478, 260, 532))
    phim1 = imagebig1.crop((28, 478, 260, 532))
    pwim = imagebig1.crop((22, 555, 260, 606))
    ccim = imagebig1.crop((22, 632, 260, 689))
    srim = imagebig1.crop((28, 711, 260, 762))
    srim1 = imagebig1.crop((32, 713, 260, 760))
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
        # if nick == 'Remark 777':
        #     lv = 14
        # else:
        #     lv = 7
    datas.append([nick, wk, rd, mp, mc, sf, sc, ph, pw, cc, sr, lv])
    if None in datas[len(datas) - 1]:
        noneflag = True
        break
    print(nick, wk, rd, mp, mc, sf, sc, ph, pw, cc, sr, lv)
    if nick == '':
        nickempty = True

# write to destination base on server if all nicks are recognized
if not nickempty and not noneflag:
    writebase(datas, grp)
elif nickempty:
    print('There are empty unrecognized nicks in the list')
else:
    print('There are unrecognized numbers in the list')

# write to destination (cards.xlsx) if all nicks are recognized
# if not nickempty and not noneflag:
#     putinxl(datas)