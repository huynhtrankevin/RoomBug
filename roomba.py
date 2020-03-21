import serial
import time


# start command which must be sent before any other command
OPCODE_START = 128

# operational modes
OPCODE_SAFE = 131
OPCODE_FULL = 132

# shutdown roomba
OPCODE_POWER = 133

# LED control
OPCODE_LEDS = 139

#actuator controls
OPCODE_DRIVE = 137
OPCODE_DRIVE_DIRECT = 145

#buttons
OPCODE_BUTTON_PRESS = 165
CLEAN_BUTTON = 0
SPOT_BUTTON = 1
DOCK_BUTTON = 2
MINUTE_BUTTON = 3
HOUR_BUTTON = 4
DAY_BUTTON = 5
SCHEDULE_BUTTON = 6
CLOCK_BUTTON = 7

# roomba button behaviors
OPCODE_CLEAN = 135

# sensor opcode and packet ID
OPCODE_SENSORS = 142
PKTID_BUMPS_WHEELDROPS = 7
PKTID_WALL = 8
PKTID_BUTTONS = 18

TURN_INPLACE_CW = 0xFFFF
TURN_INPLACE_CCW = 0x0001
DRIVE_STRAIGHT = 0x8000

IDX_LWHEELDROP = 3
IDX_RWHEELDROP = 2
IDX_LBUMP = 1
IDX_RBUMP = 0

#util functions
def get_lower(val):
    res = val & (0xFF)
    return res

def get_upper(val):
    res = (val >> 8) & (0xFF)
    return res

def constrain(val, lower_bound, upper_bound):
    res = val
    if val < lower_bound:
        res = lower_bound
        
    if val > upper_bound:
        res = upper_bound
    
    return res



class Roomba:
    def __init__(self):
        self.serial = serial.Serial(port = '/dev/serial0',baudrate = 115200)
        self.leftBumpDetected = False
        self.rightBumpDetected = False
        self.wallDetected = False
        self.powerButtonPressed = False
    
    def write_start(self):
        self.serial.write([OPCODE_START])
    
    def write_mode(self,mode):
        if(mode == OPCODE_FULL):
            self.serial.write([OPCODE_FULL])
        else:
            self.serial.write([OPCODE_SAFE])
    
    def write_LED(self,LED_bits, power_color, power_intensity):
        msg = [OPCODE_LEDS, LED_bits, power_color, power_intensity]
        self.serial.write(msg)
    
    def write_shutdown(self):
        self.serial.write([OPCODE_POWER])
    
    def write_clean(self):
        self.serial.write([OPCODE_CLEAN])
        
    def write_drive(self,velocity, radius):
        vel = constrain(velocity,-500, 500)
        if radius != TURN_INPLACE_CW & radius != TURN_INPLACE_CCW & radius != DRIVE_STRAIGHT:
            r = constrain(radius,-2000, 2000)
        else:
            r = radius

        cmd = [OPCODE_DRIVE, get_upper(vel), get_lower(vel), get_upper(r), get_lower(r)]
        self.serial.write(cmd)
    
    def write_drive_direct(self,left_velocity, right_velocity):
        lvel = constrain(left_velocity, -500, 500)
        rvel = constrain(right_velocity, -500, 500)
        cmd = [OPCODE_DRIVE_DIRECT, get_upper(rvel), get_lower(rvel), get_upper(lvel), get_lower(lvel)]
        self.serial.write(cmd)

    def read_bumps(self):
        cmd = [OPCODE_SENSORS, PKTID_BUMPS_WHEELDROPS]
        self.serial.write(cmd)

        bytes_read = self.serial.read(1)
        return bytes_read
    
    def read_buttons(self):
        cmd = [OPCODE_SENSORS, PKTID_BUTTONS]
        self.serial.write(cmd)
        
        bytes_read = self.serial.read(1)
        
        self.powerButtonPressed = bool(bytes_read[0] & bytes([(1 << CLEAN_BUTTON)])[0])
        
        if self.powerButtonPressed == True:
            # lazy hack... remove later
            print('Power Button Pressed')
            self.write_shutdown()    
        
        
        return bytes_read


