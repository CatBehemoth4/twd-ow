import PySimpleGUI as sg

import confirmation
from putinbase import baseconnect, grouplist, writebase
from reco import recognizeImages

passlayout = [[sg.Text('Login', key='loginlbl', size=(10, 1)),
               sg.pin(sg.InputText(key='log-in', size=(14, 1))),
                   sg.pin(sg.Text('', key='loginshow', visible=False, size=(14,1), text_color='yellow')),
               sg.pin(sg.Text('Password', key='passw', size=(10, 1))),
               sg.pin(sg.Input(size=(14,1), key='passfield', password_char='*')),
               sg.pin(sg.Button('Login', size=(9, 1), key='loggingin', visible=True)),
                   sg.pin(sg.Button('Change User', size=(9, 1), key='relog', visible=False))]]

grouplayout = [[sg.Combo('Group', key='groups', size=(15, 1), disabled=True), sg.Submit('Submit', key='choosegroup', disabled=True)]]

datelayout = [[sg.Input('', key='datdate', size=(12,1), disabled=True),
               sg.CalendarButton('Enter desired date', key='Ddate', disabled=True, format='%Y-%m-%d', target='datdate'),
               sg.Button('Accept date', key='Accept', disabled=True)],
              [sg.Button('Update base', key='Finalupdate', disabled=True)]]

window = sg.Window('TWD', [passlayout, grouplayout, datelayout])

while True:
    event, values = window.read()
    if event == 'loggingin':
        login = values['log-in']
        passwd = values['passfield']
        try:
            cur, conn = baseconnect(login, passwd)
            grplist = grouplist(cur, conn, mode=2)
            window['groups'].update(values = grplist)
            window['loginlbl'].update('Logged in as')
            window['log-in'].update(visible=False)
            window['log-in'].set_focus(True)
            window['loginshow'].update(login, visible=True, text_color='yellow')
            window['passw'].update(visible=False)
            window['passfield'].update(visible=False)
            window['loggingin'].update(visible=False)
            window['relog'].update(visible=True)
            window['groups'].update(disabled=False)
            window['choosegroup'].update(disabled=False)
        except:
            sg.Popup('Can''t login', 'Incorrect login')
            window['log-in'].update('')
            window['passfield'].update('')
            window['log-in'].set_focus(True)
    if event == 'relog':
        login = ''
        passwd = ''
        cur.close()
        conn.close()
        window['groups'].update(disabled=True)
        window['choosegroup'].update(disabled=True)
        window['loginlbl'].update('Login')
        window['log-in'].update('', visible=True)
        window['loginshow'].update(visible=False)
        window['passw'].update(visible=True)
        window['passfield'].update('', visible=True)
        window['loggingin'].update(visible=True)
        window['relog'].update(visible=False)
    if event == 'choosegroup':
        grup = values['groups']
        if grup != '':
            window.disable_close = True
            window['groups'].update(disabled=True)
            window['choosegroup'].update(disabled=True)
            window['relog'].update(disabled=True)
            window['loggingin'].update(disabled=True)
            dat, nam = recognizeImages(cur, conn)
            dat = confirmation.showoutputdata(dat)
            window['datdate'].update(disabled=False)
            window['Ddate'].update(disabled=False)
            window['Accept'].update(disabled=False)
        else:
            sg.popup_ok('Error', 'You must choose a group')
    if event == 'Accept':
        date = values['datdate']
        if date == '':
            sg.popup_ok('Error', 'Date should not be empty')
        else:
            window['datdate'].update(disabled=True)
            window['Ddate'].update(disabled=True)
            window['Finalupdate'].update(disabled=False)
    if event == 'Finalupdate':
        window['Finalupdate'].update(disabled=True)
        grp = grouplist(cur, conn, mode=3)[grup]
        writebase(dat, grp, date, cur, conn)
        window.disable_close = False
        window['relog'].update(disabled=False)
    if (event == sg.WIN_CLOSED) or (event == 'Close'):
        break

window.close()