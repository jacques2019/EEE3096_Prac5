import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

temp_0volt = 0.4
temp_coefficient = 0.010

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0 and 1
chan_temp = AnalogIn(mcp, MCP.P1)
chan_LDR = AnalogIn(mcp, MCP.P0)

# Read values from ADC
temp_voltage = chan_temp.voltage
temp_value = chan_temp.value

LDR_value = chan_LDR.value
LDR_voltage = chan_LDR.voltage

# Convert to Temp
temp = (temp_voltage - temp_0volt)/temp_coefficient

# Change resisitor voltage to LDR voltage
LDR_reading = 3.3 - LDR_voltage

print('Runtime\t\tTemp Reading\tTemp')
print('{0}s\t\t{1}\t\t{2:.3f}\t\t'.format(1, temp_value, temp))
print('{0}s\t\t{1}\t\t{2:.3f}\t\t'.format(1, LDR_value, LDR_reading))
