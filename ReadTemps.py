import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import math
from adafruit_mcp3xxx.analog_in import AnalogIn

mcp_0volt = 0.4
mcp_coefficient = 0.010

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

mcp_voltage = chan.voltage
mcp_value = chan.value

# Convert to Temp
temp = math.abs((mcp_voltage - mcp_0volt)/mcp_coefficient)