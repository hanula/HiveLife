
require("dht")
require("http")
require("cjson")

require("sensors")
config = require("config")

LOOP_INTERVAL_SEC = 3

function setup()
    -- setup wifi connection
    wifi.setmode(wifi.STATION)
    wifi.setphymode(wifi.PHYMODE_N)
    wifi.sleeptype(wifi.LIGHT_SLEEP)
    wifi.sta.config(config.WIFI_NAME , config.WIFI_PASSWORD)

    -- setup temp sensor
    sensors.setup()
end

-- POSTs sensor JSON data to the `config.SERVER_URL` address.
function upload_data(data)
    data = cjson.encode(data)
    print("Sending data: " .. data)

    function callback(code, data)
        if code ~= 200 then
            print("Error sending data: Code " .. code)
        end
    end

    http.post(config.SERVER_URL,
              'Content-Type: application/json\r\n',
              data,
              callback)
end


function main_loop()
    print("Checking sensors")
    data = sensors.collect_data()
    upload_data(data)
end


print("Starting up")
setup()

tmr.alarm(1, LOOP_INTERVAL_SEC * 1000, tmr.ALARM_AUTO, main_loop)

