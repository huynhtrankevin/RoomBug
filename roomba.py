import serial
import time


s = serial.Serial(port = '/dev/serial0',baudrate = 115200)

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

# sensor opcode and packet ID
OPCODE_SENSORS = 142
PKTID_BUMPS_WHEELDROPS = 7
PKTID_WALL = 8



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
def write_start():
    s.write([OPCODE_START])

def write_mode(mode):
    if(mode == OPCODE_FULL):
        s.write([OPCODE_FULL])
    else:
        s.write([OPCODE_SAFE])
    
def write_LED(LED_bits, power_color, power_intensity):
    msg = [OPCODE_LEDS, LED_bits, power_color, power_intensity]
    s.write(msg)
    
def write_shutdown():
    s.write([OPCODE_POWER])

TURN_INPLACE_CW = 0xFFFF
TURN_INPLACE_CCW = 0x0001
DRIVE_STRAIGHT = 0x8000

def write_drive(velocity, radius):
    vel = constrain(velocity,-500, 500)
    if radius != TURN_INPLACE_CW & radius != TURN_INPLACE_CCW & radius != DRIVE_STRAIGHT:
        r = constrain(radius,-2000, 2000)
    else:
        r = radius

    cmd = [OPCODE_DRIVE, get_upper(velocity), get_lower(velocity), get_upper(radius), get_lower(radius)]
    s.write(cmd)
    

def write_drive_direct(left_velocity, right_velocity):
    lvel = constrain(left_velocity, -500, 500)
    rvel = constrain(right_velocity, -500, 500)
    cmd = [OPCODE_DRIVE_DIRECT, get_upper(rvel), get_lower(rvel), get_upper(lvel), get_lower(lvel)]
    s.write(cmd)

IDX_LWHEELDROP = 3
IDX_RWHEELDROP = 2
IDX_LBUMP = 1
IDX_RBUMP = 0

def read_bumps():
    cmd = [OPCODE_SENSORS, PKTID_BUMPS_WHEELDROPS]
    s.write(cmd)
    
    bytes_read = s.read(1)
    return bytes_read
