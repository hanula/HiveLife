
PYTHON ?= python2
LUATOOL_PATH ?= libs/luatool/luatool/luatool.py
LUATOOL_BIN ?= $(PYTHON) $(LUATOOL_PATH)
PORT ?= /dev/ttyUSB0
BAUDRATE ?= 115200
DELAY ?= 0.01
LUATOOL ?= $(LUATOOL_BIN) --port $(PORT) --baud $(BAUDRATE) --delay $(DELAY)

SENSOR_FILES = $(wildcard sensor/*.lua)

sensor: $(SENSOR_FILES)
	@echo "Deployed files: $(SENSOR_FILES)"

sensor/%.lua: noop
	@echo "Uploading file: $@"
	@$(LUATOOL) --src $@ > /dev/null

noop:
