import serial
from adafruit_bno08x_rvc import BNO08x_RVC
import time

uart = serial.Serial("/dev/serial0", 115200)
rvc = BNO08x_RVC(uart)

#rvc = BNO08x_RVC(uart)

while 1:
    yaw, pitch, roll, x_accel, y_accel, z_accel = rvc.heading
    #time.sleep(1/100)
    #print('\x1b[2J')
    print("Yaw: %2.2f Pitch: %2.2f Roll: %2.2f Degrees" % (yaw, pitch, roll))
    print("Acceleration X: %2.2f Y: %2.2f Z: %2.2f m/s^2" % (x_accel, y_accel, z_accel))
