#!/usr/bin/python3
## GeeMeter COMPACT (1000 vertical pixels) for DCS:FC3 + A10C
version = 0.52

################################################
# This monstrosity was created by crash_horror
# and comes without warranty of any kind,
# read the license.
# (https://github.com/crash-horror)
################################################

from tkinter import *
from socket import *
from threading import *
from sys import platform
import time

##-------------------TK----------------------------

root = Tk()
root.title('G-Meter ' + str(version))
root.resizable(0, 0)

if sys.platform == 'win32':
    root.iconbitmap(default='favicon.ico')

w = Canvas(root, width=200, height=960, bg='black', highlightthickness=0)
w.pack()

globaldata = 0.0

serverstatus = 'DOWN'

valuelist = [(9, 'nine', 'red'),
             (8, 'eight', 'red'),
             (7, 'seven', 'orange'),
             (6, 'six', 'orange'),
             (5, 'five', 'yellow'),
             (4, 'four', 'yellow'),
             (3, 'three', 'green'),
             (2, 'two', 'green'),
             (1, 'one', 'blue'),
             (0, 'zero', 'blue'),
             (-1, 'minus', 'red')]

posit = 0

for i, j, k, in valuelist:
    w.create_rectangle(20, 10+posit, 180, 80+posit, fill="grey10", tags=j)
    w.create_text(100, 45+posit, text=i, font=('Arial', 40))
    posit += 85

w.create_text(100, 950, text=serverstatus, font=('Arial'), fill=('grey40'), tags='statusbar')
w.update()

##--------------------MAIN LOOP----------------------


def change_color():
    global globaldata, valuelist

    gee = round(globaldata)

    if gee < -1:
        gee = -1
    elif gee > 9:
        gee = 9

    for i, j, k in valuelist:
        # on lights:
        if i <= gee:
            w.itemconfig(j, fill=k)
            if gee > -1:
                w.itemconfig('minus', fill='grey10')
        # off lights:
        else:
            w.itemconfig(j, fill='grey10')

    w.update()
    w.after(10, change_color)

##--------------------SERVER----------------------


def the_server():
    global globaldata, serverstatus
    HOST = ''
    PORT = 1625
    ADDR = (HOST, PORT)
    # BUFSIZE = 512   # is this used? I don't think so...

    serv = socket(AF_INET, SOCK_STREAM)
    serv.bind((ADDR))
    serv.listen(5)

    serverstatus = 'LISTENING'
    w.itemconfig('statusbar', text=serverstatus)
    w.update()
    print('Listening...')  # debug fossil

    conn, addr = serv.accept()

    serverstatus = 'CONNECTED'
    w.itemconfig('statusbar', text=serverstatus)
    w.update()
    print('...connected!')  # debug fossil

    while True:
        data = conn.recv(512)
        if not data:
            print('Gserver SHUTDOWN!')  # debug fossil
            break
        globaldata = float(data)

    conn.close()
    serv.close()

    serverstatus = 'RESTARTING...'
    w.itemconfig('statusbar', text=serverstatus)
    globaldata = 0.0
    w.update()
    print('Restarting...')  # debug fossil

    time.sleep(5)
    the_server()

##---------------------------------------------------

t1 = Thread(target=the_server)
t1.daemon = True
t1.start()

w.after(1, change_color)

w.mainloop()
