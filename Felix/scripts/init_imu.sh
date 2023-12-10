#!/bin/bash -e
USER=$1
MISSION_ROOT=/home/$USER/mission

log () {
  $MISSION_ROOT/scripts/log.sh "$1"
}


# Try to find the IMU Mpdule with I2C. It should be on address 4a
if [[ $(i2cdetect -y 1 | grep -o "4a") == "4a" ]]; then
  log "Found IMU module at address 4a"

  cd $MISSION_ROOT/imu-reports 
  IMU_REPORT_FILE="report$2"
  touch $IMU_REPORT_FILE
  log "created file $IMU_REPORT_FILE"

  log "Initiating python IMU script"
  python3 $MISSION_ROOT/scripts/run_imu.py $USER $MISSION_ROOT/imu-reports/$IMU_REPORT_FILE
  # Check exit code and exit
  if [ $? != 0 ]; then
    log "IMU Python script crashed"
  fi
else 
  log "Could not detect any I2C devices at address 4a"
fi
