import roomba
import time

r = roomba.Roomba()
r.write_start()
# print('write start')
r.write_mode(mode=roomba.OPCODE_FULL)
# time.sleep(10)
# 

r.write_shutdown()

_TEST_LED = False
_TEST_MOTORS = True
_TEST_SENSORS = False

def test_LEDs():
    print('LED test')
    r.write_LED(4,255,255)
    print('COLOR CHANGED 1')
    time.sleep(1)
    r.write_LED(4,0,255)
    print('COLOR CHANGED 2')
    time.sleep(1)

def test_drive():
    print('Drive Test')
    for i in range(4):
        velocity = i*100
        r.write_drive(velocity, 1000)
        time.sleep(1)
    for i in range(4):
        velocity = -i*100
        r.write_drive(velocity,1000)
        time.sleep(1)

def test_sensors():
    print('Sensors Test')
    roomba.read_bumps()
    time.sleep(2)

while True:
    if _TEST_LED:
        test_LEDs()
        
    if _TEST_MOTORS:
        test_drive()
        
    if _TEST_SENSORS:
        test_sensors()

        