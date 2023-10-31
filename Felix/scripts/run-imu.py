import sys
import os
import datetime

from adafruit_blinka.agnostic import sleep

import board
import busio
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER

report_file = open(sys.argv[1], 'a')
def log(message: str):
    os.system("~/mission/scripts/log.sh \"%s\"" % message)

def report(data: str):
    time = datetime.datetime.now().time().isoformat()
    report_file.write(time + " [Report]: " + data + "\n")


i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)

log("Initiating IMU acceleration reports")
while True:
    sleep(0.5)
    accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
    report("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
