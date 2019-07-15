# RoomBug

## Configuring Raspberry Pi 3 B+ running Raspbian Stretch OS for I2C 

1. ``` sudo raspi-config ```
2. Select option 5 Interfacing Options
3. Select P5 I2C
4. Enable I2C
5. ```sudo reboot```
6. ``` sudo apt-get update && upgrade ```
7. Check that neccessary software is installed with:

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

Source: https://www.abelectronics.co.uk/kb/article/1089/i2c--smbus-and-raspbian-stretch-linux
