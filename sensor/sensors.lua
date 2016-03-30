local modname = ...
local M = {}
_G[modname] = M

require("ds18b20")
local pairs = pairs
local unpack = unpack
local dht = dht
local ds18b20 = ds18b20

-- pin setup
local DHT_PIN = 2
local DS18_TEMP_PIN = 4

setfenv(1,M)


-- DHT temperature and humidity
function sensor_1()
    status, temp, humi, _, _= dht.read(DHT_PIN)
    if status == dht.OK then
        return {temperature=temp, humidity=humi}

    elseif status == dht.ERROR_CHECKSUM then
        print( "DHT Checksum error." )
    elseif status == dht.ERROR_TIMEOUT then
        print( "DHT timed out." )
    end
end


function sensor_2()
    local temp = ds18b20.read()
    if temp < 60 then
        return {temperature=temp}
    end
end

function setup_sensor_2()
    ds18b20.setup(DS18_TEMP_PIN)
end

local sensors = {
    {"sensor_1", sensor_1, nil},
    {"sensor_2", sensor_2, setup_sensor_2}
}


function setup()
    for _, sensor in pairs(sensors) do
        local setup_fn = sensor[3];
        if (setup_fn ~= nil) then
            setup_fn()
        end
    end
end


function collect_data()
    data = {}
    for _, sensor in pairs(sensors) do
        local name, handler = unpack(sensor)
        data[name] = handler()
    end
    return data
end


return M
