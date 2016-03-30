
-- Executes `main.lua` file after 3 seconds, giving some time to eventually
-- interrupt the execution on startup.

function load_main()
    dofile("main.lua")
end

tmr.alarm(1, 3000, tmr.ALARM_SINGLE, load_main)
