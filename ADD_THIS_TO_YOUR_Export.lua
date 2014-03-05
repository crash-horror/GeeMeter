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
aircraft = LoGetObjectById(LoGetPlayerPlaneId())
MainPanel = GetDevice(0)

-- Accelerometer_main				= CreateGauge()
-- Accelerometer_main.arg_number	= 15
-- Accelerometer_main.input		= {-5.0, 10.0}
-- Accelerometer_main.output		= {0.0, 1.0}
-- Accelerometer_main.controller	= controllers.Accelerometer_main

if (aircraft.Name == "A-10C") then
		function LuaExportAfterNextFrame()
			local Gee = MainPanel:get_argument_value(15) * 15 - 5

				if Gee > 20 or Gee < 20 then
					Gee = 0
				end

			socket.try(c:send(string.format("%.2f",Gee)))
		end
	else
		function LuaExportAfterNextFrame()
			local Gee = LoGetAccelerationUnits()
			socket.try(c:send(string.format("%.2f",Gee.y)))
		end
	end

------------------------------------------------
function LuaExportStop()
	c:close()
end
------------------------------------------------
--------------END OF GEE-METER CODE-------------
------------------------------------------------