# Felix log for AURORE-II

### October 12th
Got the Rpi zero 2 delivered. Managed to boot with Raspberry PI OS (bullseye) Lite. Established ssh client

### October 14th
Failed to install circuitpython
After reinstalling the OS and retrying, I got it to work.
Blink test passed

I2C BNO08x test failed (Input/Output error)
UART wiring gives same error

### October 15th
Confirmed I2C pins are as stated in GPIO Pinout Orientation for RaspberryPi Zero 2 W.
`bash
i2cdetect -y 1
`
gives no indication that there exists an i2c bus for the IMU module.

In some cases it returns  
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f  
00:                         -- -- -- -- -- -- -- --  
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  
70: -- -- -- -- -- -- -- --  
```
indicating that the device cannot find any i2c bus.

In other cases it returns
`
-bash: /usr/sbin/i2cdetect: Input/output error
`
