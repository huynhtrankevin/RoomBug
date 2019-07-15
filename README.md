# RoomBug

## Description

RoomBug is an affordable mobile vacuuming robot inspired by the commercial Roomba robots and is capable of autonomous navigation throughout user specified regions of the environment. 

The system runs on a Raspberry Pi 3 B+ and is actuated by low-cost hobby DC motors. It navigates by using a light weight SLAM algorithm on sensor measurements from a PiCamera module, LIDAR sensor, and MPU6050 IMU sensor to perform position estimation.


## Table of Contents

1. Setting up the MPU6050 
2. Setting up the motor driver 

## Setting up the MPU6050

### Configuring Raspberry Pi 3 B+ running Raspbian Stretch OS for I2C 

**1**. ``` sudo raspi-config ```

**2**. Select option 5 Interfacing Options

**3**. Select P5 I2C

**4**. Enable I2C

**5**. ```sudo reboot```

**6**. ``` sudo apt-get update && upgrade ```

**7**. Check that neccessary software is installed with:

  ```
  sudo apt-get install python-smbus python3-smbus python-dev python3-dev i2c-tools
  ```


For kernel versions 3.18 or later, you will also need to update the /boot/config.txt file.
You can check your version by:

```
cat /etc/debian_version
```

And your OS release by:

```
cat /etc/os-release
```

**8**. If you were running 3.18 or later, we'll need to enable i2c in the config file.

Open the config file with:

```
sudo nano /boot/config.txt
```

and add the following text to the bottom of the file:

```
dtparam=i2c1=on
```
**9**. Make sure that 'pi' user is added to the i2c group so that we could use I2C tools owithout being in root

```
sudo adduser pi i2c
```

### Setting the I2C Bus speed

**1**. We can configure the I2C bus speed to be 100 kbit/s (standard mode), 400 kbits/s (full speed), 1 Mbit/s (fast mode), and 3.2 Mbit/s (high speed). We'll configure our bus speed to be 1 MHz.

Open the config.txt file:
```
sudo nano /boot/config.txt
```

and add the following text to the bottom:

```
dtparam=i2c_baudrate=1000000
```


**2**. For Pi's 3B, 3B+ and Zero W, the clock for the I2C controller is linked to the VPU core which means that the clock frequency may vary depending on the VPU load. To solve this, we'll fix the VPU core frequency to a constant frequency.

Open the config file:

``` 
sudo nano /boot/config.txt
```
and add:

``` 
core_freq = 250
```
to the bottom of the file. We fixed the VPU's core frequency to the default frequency to avoid any issues with overclocking.

**3**. Now reboot the pi for the configurations to take effect:

```
sudo reboot now
```

### Wiring it up

ADD IMAGES AND DIRECTIONS

### Testing

**1**. To test if everything worked, run the mpu6050test.py program:

```
python mpu6050test.py
```

You should see something like:

**Sources**:

https://www.abelectronics.co.uk/kb/article/1089/i2c--smbus-and-raspbian-stretch-linux

https://www.raspberrypi.org/documentation/configuration/config-txt/overclocking.md
