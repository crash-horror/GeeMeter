## GeeMeter

version = 0.5

from tkinter import *
from socket import *
from threading import *
import time

##-------------------TK----------------------------

root = Tk()
root.title('G-Meter ' + str(version))
w = Canvas(root, width=200, height=1120, bg='black')
w.pack()

globaldata = 0.0

serverstatus = 'DOWN'

posit = 0
textposit = 0
geelist =   ['nine', 'eight', 'seven',  'six',    'five',   'four',   'three', 'two',   'one', 'zero',  'minus']
colorlist = ['red',  'red',   'orange', 'orange', 'yellow', 'yellow', 'green', 'green', 'blue', 'blue', 'red']
numlist = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1]

for i in geelist:
	w.create_rectangle(20, 10+posit, 180, 80+posit, fill="grey10", tags=i)
	posit += 100

for i in numlist:
	w.create_text(100, 45+textposit, text=i, font=('Arial', 40))
	textposit += 100

w.create_text(100, 1110, text = serverstatus, font=('Arial'), fill=('grey40'), tags='statusbar')
w.update()

##--------------------MAIN LOOP----------------------

def change_color():
	global geelist, numlist, globaldata

	gee_in = globaldata
	gee = round(gee_in)

	if gee < -1:
		gee = -1
	elif gee > 9:
		gee = 9

	onlightlist = geelist[numlist.index(gee):]

	for on in onlightlist:
		w.itemconfig(on, fill=colorlist[geelist.index(on)])

	if gee > -1:
		offlightlist = geelist[:numlist.index(gee)] + ['minus']
	else:
		offlightlist = geelist[:numlist.index(gee)]

	for off in offlightlist:
		w.itemconfig(off, fill='grey10')

	w.update()
	w.after(10, change_color)

##--------------------SERVER----------------------

def the_server():
	global globaldata, serverstatus, w
	HOST = ''
	PORT = 1625
	ADDR = (HOST,PORT)
	BUFSIZE = 512

	serv = socket(AF_INET,SOCK_STREAM)
	serv.bind((ADDR))
	serv.listen(5)

	serverstatus = 'LISTENING'
	w.itemconfig('statusbar', text=serverstatus)
	w.update()
	print('Listening...')

	conn,addr = serv.accept()

	serverstatus = 'CONNECTED'
	w.itemconfig('statusbar', text=serverstatus)
	w.update()
	print('...connected!')

	while True:
	    data = conn.recv(512)
	    if not data:
	    	print('Gserver SHUTDOWN!')
	    	break
	    globaldata = float(data)

	conn.close()
	serv.close()

	serverstatus = 'RESTARTING...'
	w.itemconfig('statusbar', text=serverstatus)
	globaldata = 0.0
	w.update()
	print('Restarting...')

	time.sleep(5)
	the_server()

##---------------------------------------------------

t1 = Thread(target=the_server)
t1.daemon = True
t1.start()

w.after(1, change_color)

w.mainloop()



