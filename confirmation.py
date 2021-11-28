from tkinter import *
from tkinter.ttk import *

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

# print(namechoice(('1', '3', '5', '6')))
