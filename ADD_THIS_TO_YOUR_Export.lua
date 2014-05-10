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
	c:close()
end
------------------------------------------------
--------------END OF GEE-METER CODE-------------
------------------------------------------------