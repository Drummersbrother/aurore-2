#!/bin/bash -e
VERBOSE=true

# Ensure the existance of the "logs" directory
if [ ! -d logs ]; then
  echo "Could not find 'logs' directory... Creating"
  mkdir logs;
fi

# Ensure the existance of the "imu-reports" directory
if [ ! -d imu-reports ]; then
  echo "Could not find 'imu-reports' directory... Creating"
  mkdir imu-reports
fi


# INIT LOG

# Create new log file
cd ~/logs
EXISTING_FILES=$(ls -1q log* | wc -l)
LOG_FILE="log$EXISTING_FILES"
touch $LOG_FILE

# Create callable log executable to be used outside of this file
if [ ! -f ~/scripts/log.sh ]; then
  echo "Creating log executable"
  touch ~/scripts/log.sh
  chmod +x ~/scripts/log.sh
else
  # clear file
  > ~/scripts/log.sh;
fi

echo "echo \"\$(date) [Log]: \$1\">> ~/logs/$LOG_FILE" >> ~/scripts/log.sh

if [ VERBOSE ]; then
  echo "echo \"$1\"" >> ~/scripts/log.sh
fi

# Function to log message to the master log file for this session
log () {
  ~/scripts/log.sh "$1"
}


#INIT IMU

# Try to find the IMU Mpdule with I2C. It should be on address 4a
if [ -n $(i2cdetect -y 1 | grep 4a) ]; then 
  log "Could not detect any I2C devices at address 4a"
else
  log "Found IMU module at address 4a"

  cd ~/imu-reports
  IMU_REPORT_FILE="report$EXISTING_FILES"
  touch $IMU_REPORT_FILE

  log "Initiating python IMU script"
  python3 ~/scripts/run-imu.py ~/imu-reports/$IMU_REPORT_FILE
fi
