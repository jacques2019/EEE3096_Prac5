import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import time
import RPi.GPIO as GPIO

temp_0volt = 0.4
temp_coefficient = 0.010

chan_temp = None
chan_LDR = None
btn_delay = 22

start_temp_time = 0
start_LDR_time = 0

delayTime = 10

def read_temp_thread():
    global chan_temp
    global start_temp_time
    global delayTime

    thread = threading.Timer(delayTime, read_temp_thread)
    thread.daemon = True
    thread.start()

    currentTime = int(round(time.time()))
    if (start_temp_time == 0):
        start_temp_time = currentTime

    # Read values from ADC
    temp_voltage = chan_temp.voltage
    temp_value = chan_temp.value

    # Convert to Temp
    temp = (temp_voltage - temp_0volt)/temp_coefficient

    # Print temp readings
    print('Runtime\t\tTemp Reading\tTemp')
    print('{0:.0f}s\t\t{1}\t\t{2:.3f}\t\t C'.format((currentTime - start_temp_time), temp_value, temp))

def read_LDR_thread():
    global chan_LDR
    global start_LDR_time
    global delayTime

    thread = threading.Timer(delayTime, read_LDR_thread)
    thread.daemon = True
    thread.start()

    currentTime = int(round(time.time()))
    if (start_LDR_time == 0):
        start_LDR_time = currentTime

    # Read values from ADC
    LDR_value = chan_LDR.value
    LDR_voltage = chan_LDR.voltage

    # Change resisitor voltage to LDR voltage
    LDR_reading = 3.3 - LDR_voltage

    # Print LDR readings
    print('Runtime\t\tLDR Reading\tLDR Voltage')
    print('{0:.0f}s\t\t{1}\t\t{2:.3f}\t\t V'.format((currentTime - start_LDR_time), LDR_value, LDR_reading))

def setup():
    global chan_temp
    global chan_LDR

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # Create an analog input channel on pin 0 and 1
    chan_temp = AnalogIn(mcp, MCP.P1)
    chan_LDR = AnalogIn(mcp, MCP.P0)

    GPIO.setup(btn_delay, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn_delay, GPIO.FALLING, callback=btn_delay_callback, bouncetime=250)
    
def btn_delay_callback(channel):
    global delayTime

    if (delayTime == 10):
        delayTime = 5
    elif (delayTime == 5):
        delayTime = 1
    elif (delayTime == 1):
        delayTime = 10

    print("pressed")

if __name__ == "__main__":
    setup()
    read_LDR_thread()
    read_temp_thread()

    # Run indefinitely
    while True:
        pass