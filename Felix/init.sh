#!/bin/bash -e
VERBOSE=true


cd mission
MISSION_ROOT=~/mission


# Ensure the existance of the "logs" directory
if [ ! -d logs ]; then
  if [ VERBOSE ]; then
    echo "Could not find 'logs' directory... Creating"
  fi

  mkdir logs;
fi

# Ensure the existance of the "imu-reports" directory
if [ ! -d imu-reports ]; then
  if [ VERBOSE ]; then
    echo "Could not find 'imu-reports' directory... Creating"
  fi

  mkdir imu-reports
fi


# INIT LOG

# Create new log file
cd $MISSION_ROOT/logs
EXISTING_FILES=$(ls -1q log* | wc -l)
LOG_FILE="log$EXISTING_FILES"
touch $LOG_FILE

# Create callable log executable to be used outside of this file
if [ ! -f $MISSION_ROOT/scripts/log.sh ]; then
  if [ VERBOSE ]; then
    echo "Creating log executable"
  fi

  touch $MISSION_ROOT/scripts/log.sh
  chmod +x $MISSION_ROOT/scripts/log.sh
else
  # clear file
  > $MISSION_ROOT/scripts/log.sh;
fi

# Logic for the log script
echo "echo \"\$(date) [Log]: \$1\">> $MISSION_ROOT/logs/$LOG_FILE" >> $MISSION_ROOT/scripts/log.sh

if [ VERBOSE ]; then
  echo "echo \"$1\"" >> $MISSION_ROOT/scripts/log.sh
fi

# Function to log message to the master log file for this session
log () {
  $MISSION_ROOT/scripts/log.sh "$1"
}


#INIT IMU

# Try to find the IMU Mpdule with I2C. It should be on address 4a
if [ -n $(i2cdetect -y 1 | grep 4a) ]; then 
  log "Could not detect any I2C devices at address 4a"
else
  log "Found IMU module at address 4a"

  cd $MISSION_ROOT/imu-reports
  IMU_REPORT_FILE="report$EXISTING_FILES"
  touch $IMU_REPORT_FILE

  log "Initiating python IMU script"
  python3 $MISSION_ROOT/scripts/run-imu.py $MISSION_ROOT/imu-reports/$IMU_REPORT_FILE
fi
