import roomba
import sched
import time
import threading
import DFPlayerTest as df

# request every 20ms
requestInterval = 0.03


threadLock = threading.Lock()
bytes_read = bytes([0])
class SensorData:
    def __init__(self):
        self.bytes_read = bytes([0])
        
class myThread(threading.Thread):
    def __init__(self, threadID,name, func, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.func = func
        self.args = args
    def run(self):
        self.func(self.args)



def runRequestSensorData(sDat):
    roomba.write_start()
    roomba.write_mode(mode=roomba.OPCODE_FULL)
    print('Roomba in Full Mode')
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(requestInterval,1,requestSensorData,argument=(scheduler,sDat,))
    scheduler.run()
    
def requestSensorData(scheduler,sDat):
    threadLock.acquire(blocking=1)
    global bytes_read
    #bytes_read = [0]
    bytes_read = roomba.read_bumps()
    #print(bytes_read)
    
    threadLock.release()
    # start event scheduler over
    scheduler.enter(requestInterval,1,requestSensorData,argument=(scheduler,sDat,))
    

def respondToBumps(sDat):
    global bytes_read
    threadLock.acquire(blocking=1)
    print('Respond')
    #print(bytes_read)
    leftBumpDetected = bytes_read[0] & (bytes([1 << roomba.IDX_LBUMP])[0])
    rightBumpDetected = bytes_read[0] & (bytes([1 << roomba.IDX_RBUMP])[0])
 
    if leftBumpDetected == 2:
        print('Bump Detected')
        bytes_read = bytes([0])
        df.play(1,2)

    threadLock.release()
    time.sleep(0.02)

def runMain(sDat):
    
    while True:
        respondToBumps(sDat)
        

sDat = SensorData()
thread1 = myThread(1,"SensorReadingThread",runRequestSensorData,args = sDat)
thread2 = myThread(2,"RespondThread",runMain,args=sDat)
thread1.start()
thread2.start()



    
    
    
    







#
#while True:
#    print('while loop')
#    if sensorData.bytesBumpReadings[0] & bytes([1 << roomba.IDX_LBUMP])[0]:
#        print('left bump detected')
#    if sensorData.bytesBumpReadings[0] & bytes([1 << roomba.IDX_RBUMP])[0]:
#        print('left bump detected')