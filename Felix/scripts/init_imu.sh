MISSION_ROOT=~/mission

log () {
  $MISSION_ROOT/scripts/log.sh "$1"
}


# Try to find the IMU Mpdule with I2C. It should be on address 4a
if [ -n $(i2cdetect -y 1 | grep 4a) ]; then
  log "Could not detect any I2C devices at address 4a"
else 
  log "Found IMU module at address 4a"

  cd $MISSION_ROOT/imu-reports 
  IMU_REPORT_FILE="report$1"
  touch $IMU_REPORT_FILE

  log "Initiating python IMU script"
  python3 $MISSION_ROOT/scripts/run_imu.py $MISSION_ROOT/imu-reports/$IMU_REPORT_FILE
  # Check exit code and exit
  if [ $? != 0 ]; then
    log "IMU Python script crashed"
  fi
fi
