## GeeMeter
## Info at the bottom.
version = 0.5

from tkinter import *
from socket import *
from threading import *
import time

##-------------------TK----------------------------

root = Tk()
root.title('Gee Meter')
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
	    if len(data) == 0 or len(data) > 8:
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

#####################################################
#
# Notes:
#
#	This script creates a fixed 200 by 1120 window,
#   which means you need at least 1200 vertical
#	screen resolution on your second monitor.
#   Future versions might have a scalable window.
#
#   In case you want to run this script on another
#	computer, you just need to change the IP address
#   in the Export.lua (see below) from
#	host = "localhost" to host = xxx.xxx.xxx.xxx
#	or host = "your_computer_network_name"
#	according to your lan address you run GeeMeter on.
#
#
# Troubleshoot:
#
# 	In case of the server not starting/restarting:
# 		Open windows task manager and kill the process
#			'pythonw.exe'.
# 	The reason is that the server may not have terminated properly.
#
########################################################
#
# For this script to work you need to add the
# following lines at the end of your Export.lua file located at:
# C:\Users\~\Saved Games\DCS\Scripts\Export.lua
#
# or for the beta version:
# C:\Users\~\Saved Games\DCS.openbeta\Scripts\Export.lua
#
# If it does not exist, just create it, (the "Scripts" folder too).
#
#
""" # !!! do not include this line !!!

------------------------------------------------
------------START OF GEE-METER CODE-------------
------------------------------------------------
function LuaExportStart()
	package.path  = package.path..";.\\LuaSocket\\?.lua"
	package.cpath = package.cpath..";.\\LuaSocket\\?.dll"
	socket = require("socket")
	host = "localhost"
	port = 1625
	c = socket.try(socket.connect(host, port))
	c:setoption("tcp-nodelay",true)
end
------------------------------------------------
function LuaExportAfterNextFrame()
	local Gee = LoGetAccelerationUnits() 
	socket.try(c:send(string.format("%+.2f",Gee.y)))
end
------------------------------------------------
function LuaExportStop()
	socket.try(c:send("123456789"))
	c:close()
end
------------------------------------------------
--------------END OF GEE-METER CODE-------------
------------------------------------------------

""" # !!! do not include this line !!!

