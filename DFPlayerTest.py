import serial
import time
import pigpio
import RPi.GPIO as GPIO

TX = 19
RX = 26

BusyPin = int(3)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BusyPin, GPIO.IN)

pi = pigpio.pi()
pi.set_mode(TX,pigpio.OUTPUT)
pigpio.exceptions = False

pi.bb_serial_read_close(RX)

# fatal exceptions on

pigpio.exceptions = True
pi.wave_clear()


START = 0x7E
VER = 0xFF
DATLEN = 0x06
END = 0xEF
ACK = 0x00


CMD_SPEC_FOLDER_PLAYBACK = 0x0F
CMD_SPEC_VOLUME = 0x06   #0-30 
CMD_PAUSE = 0x0E
CMD_RESUME = 0x0D

def write_command(cmd, param1, param2):
    checksum = -(VER + DATLEN + cmd + ACK + param1 + param2)
    msg = [START, VER, DATLEN, cmd, ACK, param1, param2, (checksum >> 8) & 0xFF, checksum & 0xFF, END]
    print(msg)
    #s.write(msg)
    pi.wave_add_serial(TX, 9600, msg)
    wid=pi.wave_create()
    pi.wave_send_once(wid)   # transmit serial data
    pi.wave_delete(wid)


def play(folder, track):
    write_command(CMD_SPEC_FOLDER_PLAYBACK,folder,track)


def setVolume(vol):
    write_command(CMD_SPEC_VOLUME,0x00,vol)

def pause():
    write_command(CMD_PAUSE, 0x00,0x00)
 
def resume():
    write_command(CMD_RESUME,0x00,0x00)
    
def isPlaying():
    return GPIO.input(BusyPin)

play(1,1)