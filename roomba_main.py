import roomba
import sched
import time

# request every 15ms
requestInterval = 0.020

# container for sensor data retrieved from roomba
class SensorData:
    def __init__(self):
        # do stuff
        self.bytesBumpReadings = []


def requestSensorData(sensorData, scheduler):
    print(sensorData.bytesBumpReadings)
    sensorData.bytesBumpReadings = roomba.read_bumps()
    print(sensorData.bytesBumpReadings)
    # start event scheduler over
    scheduler.enter(requestInterval,1,requestSensorData,argument=(sensorData,scheduler,))


roomba.write_start()
roomba.write_mode(mode=roomba.OPCODE_FULL)
roomba.write_shutdown()

sensorData = SensorData()
scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(requestInterval,1,requestSensorData,argument=(sensorData,scheduler,))
scheduler.run()

while True:
    print('while loop')
    if sensorData.bytesBumpReadings[0] & bytes([1 << roomba.IDX_LBUMP])[0]:
        print('left bump detected')
    if sensorData.bytesBumpReadings[0] & bytes([1 << roomba.IDX_RBUMP])[0]:
        print('left bump detected')
        
        
