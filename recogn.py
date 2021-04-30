from PIL import Image, ImageFilter
import pytesseract
from xlmodule import returnnicks, putinxl
from putinbase import writebase, getnicks, newNick
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

grp = 1

# enter password for root user
# passwd = getpass('Enter password: ')
passwd = 'Ly)vwW-D2.c)o0Hp'
# getting list of correct nicknames
nicksAll = getnicks(passwd)
nicks = [nk[0] for nk in nicksAll]
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
    imagesmall = imagebig.crop((392, 297, 808, 366))
    imagesmall1 = imagebig.crop((390, 297, 678, 366))
    imagesmall2 = imagebig.crop((390, 297, 678, 366))
    imagesmall = negate(imagesmall)
    imagesmall1 = imagesmall1.filter(ImageFilter.EDGE_ENHANCE)
    imagesmall = imagesmall.filter(ImageFilter.EDGE_ENHANCE)
    #imagesmall2 = imagesmall2.filter(ImageFilter.SHARPEN)
    imagesmall2 = imagesmall2.filter(ImageFilter.EDGE_ENHANCE)
    #imagesmall2 = negate(imagesmall2)
    # imagesmall1 = negate(imagesmall1)
    # imagesmall1 = imagesmall1.filter(ImageFilter.EDGE_ENHANCE)
    # select fragment for nickname
    imagebig1 = imagebig.crop((174, 1317, 447, 2097))
    #imagebig1 = negate(imagebig1)
    # reveal nick in image
    imagesmall.save('0.jpg')
    imagesmall1.save('1.jpg')
    imagesmall2.save('2.jpg')
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
    print (1, nicke, nickt, nickr)

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
        print(2, nicke, nickt, nickr)
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
            print(3, nicke, nickt, nickr)
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
print(nick)
