from getpass import getpass
from putinbase import delNick

passwd = getpass('Enter password:')
nick = int(input('Enter nickname to remove: '))
delNick(nick, passwd)