import roomba as r
import sched
import time
import threading
import DFPlayerTest as df

# request every 20ms
requestInterval = 0.03

# util function
def stateDelay(delay):
        i = 0
        waitTime = 1000000*delay
        while (i < waitTime):
            i = i + 1
            

threadLock = threading.Lock()
# thread class    
class myThread(threading.Thread):
    def __init__(self, threadID,name, func, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.func = func
        self.args = args
    def run(self):
        self.func(self.args)

# class to implement state machine
class StateMachine:
    def __init__(self, roomba):
        self.passive_state = 0
        self.pissed_state_1 = 1
        self.pissed_state_2 = 2
        self.current_state = self.passive_state
        self.bumpCount = 0
        self.roomba = roomba
        self.timeThresh = 3 # in time units returned by time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        self.timeSinceLastBump = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
    
    
            
    def updateState(self):
        if self.roomba.leftBumpDetected | self.roomba.rightBumpDetected:
            print('bump detected')
            self.timeSinceLastBump = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
            
            if self.current_state == self.passive_state:
                self.current_state = self.pissed_state_1
                
#             elif self.current_state == self.pissed_state_1:
#                 self.current_state = self.pissed_state_2
#                 
#             elif self.current_state == self.pissed_state_2:
#                 self.current_state = self.passive_state
        
        #print(self.current_state)
        
                
    def runState(self):
        if self.current_state == self.passive_state:
            print('passive')
            
        if self.current_state == self.pissed_state_1:
            self.roomba.write_mode(mode=r.OPCODE_FULL)
            
            # back up
            print('Backing Up')
            self.roomba.write_drive_direct(int(-200),int(-200))
            
            stateDelay(7)    
            #time.sleep(5)
            
            print('Stopping Now')
            # stop
            self.roomba.write_drive(velocity=0, radius=r.DRIVE_STRAIGHT)
            stateDelay(7)    
            print('playing audio')
            # play audio 1 until audio done
            df.play(1,1)
            
            # spin in a circle
            self.roomba.write_drive(velocity=200,radius=r.TURN_INPLACE_CW)
            
            stateDelay(7)
            
            # stop
            self.roomba.write_drive(velocity=0,radius=r.TURN_INPLACE_CW)
            
            #roomba.write_clean()
           
            
            self.current_state = self.passive_state
            
            self.roomba.leftBumpDetected = False
            self.roomba.rightBumpDetected = False
        
        self.roomba.leftBumpDetected = False
        self.roomba.rightBumpDetected = False
        self.current_state = self.passive_state
                

# bumps reading interval
dt = 0.2
def startReadingBumps(roomba):
    # send start command to roomba before any other commands
    roomba.write_start()
    
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(requestInterval,dt,requestBumps,argument=(scheduler,roomba,))
    scheduler.run()
    
def requestBumps(scheduler,roomba):
    # acquire lock
    threadLock.acquire(blocking=1)
    
    # read bumps and wheel drops from roomba
    bytes_read = roomba.read_bumps()
    roomba.leftBumpDetected = bool(bytes_read[0] & (bytes([1 << r.IDX_LBUMP])[0]))
    roomba.rightBumpDetected = bool(bytes_read[0] & (bytes([1 << r.IDX_RBUMP])[0]))
    
    # hacky insertion... remove later
    roomba.read_buttons()
    
    # release lock
    threadLock.release()
    
    # start event scheduler over
    scheduler.enter(requestInterval,dt,requestBumps,argument=(scheduler,roomba,))
        
def runStateMachine(roomba):
    stateMachine = StateMachine(roomba)
    
    while True:
        threadLock.acquire(blocking=1)
        stateMachine.updateState()
        stateMachine.runState()
        threadLock.release()
        time.sleep(0.05)

roomba = r.Roomba()
thread1 = myThread(1,"SensorReadingThread",startReadingBumps, args = roomba)
thread2 = myThread(2,"StateMachineThread",runStateMachine, args=roomba)
thread1.start()
thread2.start()



    
    
    
    







#
#while True:
#    print('while loop')
#    if sensorData.bytesBumpReadings[0] & bytes([1 << roomba.IDX_LBUMP])[0]:
#        print('left bump detected')
#    if sensorData.bytesBumpReadings[0] & bytes([1 << roomba.IDX_RBUMP])[0]:
#        print('left bump detected')