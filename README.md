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

Source: https://www.abelectronics.co.uk/kb/article/1089/i2c--smbus-and-raspbian-stretch-linux
