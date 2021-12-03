from tkinter import *
from tkinter.ttk import *
import PySimpleGUI as sg


class a(object):
    def __init__(self):
        a.flg = False
        a.pressed = False
        vlu = StringVar(self, None)

class plrCh(object):
    def __init__(self, it):
        self.retr = None
        wnd  = Tk()
        super().__init__()
        self.items = it

        def ret():
            if var.get() == '4':
                self.retr = customVar.get()
            else:
                self.retr = self.items[int(var.get())]
            wnd.destroy()

        var = StringVar(wnd, None)
        customVar = StringVar(wnd, None)
        for i in range(4):
            Radiobutton(wnd, text=self.items[i], variable=var, value=i).grid(row=i, column=0)
        Radiobutton(wnd, text='', variable=var, value=4).grid(row=4, column=0)
        Entry(wnd, text='', textvariable=customVar).grid(row=4, column=1)
        Button(wnd, text='Submit', command=ret).grid(row=5, column=0)
        wnd.mainloop(1)

def confir():
    confWnd = Tk()
    confWnd.title = 'Confirm'
    flag = a()
    def yes():
        confWnd.destroy()
        flag.flg = True
        return flag.flg
    def no():
        confWnd.destroy()
        flag.flg = False
        return flag.flg
    label = Label(confWnd, text='Are your sure want to update the base?')
    label.grid(row=0, column=1)
    btnY = Button(confWnd, text='Yes', command=yes)
    btnY.grid(row=1, column=0)
    btnN = Button(confWnd, text='No', command=no)
    btnN.grid(row=1, column=1)
    confWnd.mainloop()


def namechoice(nicks):
    q = plrCh(nicks)
    return q.retr


def confsg(nicks):
    sg.theme('Tan')
    layout = [[sg.Radio(nicks[0], '1', default=True)],
             [sg.Radio(nicks[1], '1')],
             [sg.Radio(nicks[2], '1')],
             [sg.Radio(nicks[3], '1')],
             [sg.Radio('', '1'), sg.InputText(key='custnick', size=(14,1))],
             [sg.Button('Submit', key='Submit')]]
    chnickwin = sg.Window('Choose nick', layout, disable_close=True)
    while True:
        events, values = chnickwin.read()
        if events == 'Submit':
            finish = True
            if values[4]:
                nick = values['custnick']
            elif values[3]:
                nick = nicks[3]
            elif values[2]:
                nick = nicks[2]
            elif values[1]:
                nick = nicks[1]
            else:
                nick = nicks[0]
            if nick == '':
                sg.popup_ok('Error', 'You must enter non-empty nick.')
                finish = False
            if finish:
                break
        if events == sg.WIN_CLOSED:
            pass
    chnickwin.close()
    return nick


def sggetint(nick, fname, base):
    sg.theme('Tan')
    base.replace('_', ' ')
    layout = [[sg.Text('Unknown digit, the %s of player "%s" is not recognized. Enter it from file %s' % (base, nick, fname))],
              [sg.InputText(key='number')],
              [sg.Button('Submit', key='Submit')]]
    askdigitwin = sg.Window('Unknown digit', layout, disable_close=True)

    while True:
        events, values = askdigitwin.read()
        if events == sg.WIN_CLOSED:
            pass
        elif events == 'Submit':
            finish = True
            num = values['number']
            try:
                num = int(num)
                if num < 0:
                    sg.popup_ok('Error', 'You must enter positive integer')
                    finish = False
            except:
                sg.popup_ok('Error', 'You must enter integer')
                finish = False
            if finish:
                break
    askdigitwin.close()
    return num


def sgchooseplayer(possplay):
    sg.theme('Tan')
    layout = list()
    layout.append([sg.Text('More than one player "%s" found in base. Choose correct.' % possplay[0][0])])
    for player in possplay:
        layout.append([sg.Radio(player[0] + ', number ' + str(player[1]),1)])
    layout.append([sg.Button('Submit', key='Submit')])
    askcorrpl = sg.Window('Choose right player', layout, disable_close=True)

    while True:
        events, values = askcorrpl.read()
        if events == sg.WIN_CLOSED:
            pass
        elif events == 'Submit':
            finish = False
            for i in values:
                if values[i]:
                    num = possplay[i][1]
                    finish = True
                    break
            if finish:
                break
            else:
                sg.popup_ok('Error', 'You must choose anyone to continue')

    askcorrpl.close()
    return num


def showoutputdata (data):
    layout = list()
    for i in range(len(data[0])):
        col = list()
        for j in range(len(data)):
            if i == 0:
                col.append([sg.InputText(size=(11, 1), default_text=str(data[j][i]), disabled=True)])
            else:
                col.append([sg.InputText(size=(11, 1), default_text=str(data[j][i]))])
        layout.append(sg.Column(col))
    layout = [[layout], [sg.Button('Submit', key='SubOut')]]
    windout = sg.Window('', layout, disable_close=True)
    while True:
        events, values = windout.read()
        if events == sg.WIN_CLOSED:
            pass
        elif events == 'SubOut':
            finish = True
            for i in values:
                data[i % len(data)][i // len(data)] = values[i]
                if values[i] == '':
                    sg.popup_ok('Error', 'No empties allowed, check data and try again')
                    finish = False
                    break
                elif i // len(data) != (len(data[0]) - 1):
                    try:
                        data[i % len(data)][i // len(data)] = int(data[i % len(data)][i // len(data)])
                    except:
                        sg.popup_ok('Error', 'All columns except yhe last should be integer, check and try again.')
                        finish = False
                        break
            if finish:
                break
    windout.close()
    return data

# dt = [[1, 2, 3, 0], [7, 5, 6, 12], [3, 3, 3, 3], [56, 2, 7, 666]]
# print(dt)
# data = showoutputdata(dt)
# print(data)

