GeeMeter
------------------------------------------------


 Notes:

	This script creates a fixed 200 by 1120 window,
   which means you need at least 1200 vertical
	screen resolution on your second monitor.
   Future versions might have a scalable window.

   In case you want to run this script on another
	computer, you just need to change the IP address
   in the Export.lua (see below) from
	host = "localhost" to host = xxx.xxx.xxx.xxx
	or host = "your_computer_network_name"
	according to your lan address you run GeeMeter on.


 Troubleshoot:

 	In case of the server not starting/restarting:
 		Open windows task manager and kill the process
			'pythonw.exe'.
 	The reason is that the server may not have terminated properly.

------------------------------------------------

 For this script to work you need to add the
 following lines at the end of your Export.lua file located at:
 C:\Users\~\Saved Games\DCS\Scripts\Export.lua

 or for the beta version:
 C:\Users\~\Saved Games\DCS.openbeta\Scripts\Export.lua

 If it does not exist, just create it, (the "Scripts" folder too).


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


