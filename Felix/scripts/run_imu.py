import sys
import os
import datetime

from adafruit_blinka.agnostic import sleep

import traceback
import board
import busio
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER, BNO_REPORT_GAME_ROTATION_VECTOR

USER = os.environ["USER"]


def log(message: str):
    os.system('/home/%s/mission/scripts/log.sh "%s"' % (USER, message))


def report(report_type: str, data: str):
    time = datetime.datetime.now().time().isoformat()
    report_file.write(time + " [" + report_type + " Report]: " + data + "\n")


i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR)

log("Initiating IMU acceleration reports")
while True:
    sleep(0.5)
    try:
        with open(sys.argv[2], "a") as report_file:
            # Acceleration including gravity
            accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
            report("Acceleration", ("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z)))
            # Rotation in degrees/s
            rot_x, rot_y, rot_z = bno.gyro  # pylint:disable=no-member
            report("Rotation", ("X: %0.6f  Y: %0.6f Z: %0.6f  rad/s" % (rot_x, rot_y, rot_z)))
            # Quaternion heading without reference or tilt compensation
            rot_quat_x, rot_quat_y, rot_quat_z, rot_quat_w = bno.game_quaternion  # pylint:disable=no-member
            report("Quaternion", ("X: %0.6f  Y: %0.6f Z: %0.6f W: %0.6f" % (rot_quat_x, rot_quat_y, rot_quat_z, rot_quat_w)))
            # Magnetic field measurements on the X, Y, and Z axes
            mag_x, mag_y, mag_z = bno.magnetic
            report("Magnetic", ("X: %0.6f  Y: %0.6f  Z: %0.6f" % (mag_x, mag_y, mag_z)))

        # log("successfully reported IMU readings")
    except:
        log("Failed to log IMU report")
        # print full traceback to string
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log(f"IMU Exception: {exc_type}, {exc_value}")
        log(f"IMU Traceback: {traceback.format_exc()}")

        continue
