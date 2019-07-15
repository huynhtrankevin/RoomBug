from mpu6050 import mpu6050
import time

# test code to ensure that the MPU6050 works

slave_addr = 0x68

mpu = mpu6050(slave_addr)

while 1:
    accel_dat = mpu.get_accel_data()
    print ("acc_x = {} || acc_y = {} || acc_z = {}".format(accel_dat['x'],accel_dat['y'],accel_dat['z']))
    time.sleep(1)

