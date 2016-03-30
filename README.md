
HiveLife - Beehive monitoring with ESP8266 and NodeMCU
======================================================

Uses ESP8266 with connected sensors to send information about temperature and humidity inside the hive.

Usage
-----
* Copy `sensor/config.lua.example` to `sensor/config.lua` and edit it with your server address and local WIFI credentials.
* Use `make sensor` to upload NodeMCU code to the device.


TODO
----
* Add a server for receiving and storing sensor data.
* Add frontend with hive status dashboard.
