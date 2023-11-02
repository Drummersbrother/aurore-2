#!/bin/bash -e
VERBOSE=true

MISSION_ROOT=~/mission


# Ensure the existance of the "logs" directory
mkdir -p $MISSION_ROOT/logs;

# Ensure the existance of the "imu-reports" directory
mkdir -p $MISSION_ROOT/imu-reports

# Ensure the existance of the "camera-footage" directory
mkdir -p $MISSION_ROOT/camera-footage


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
try_init_imu() {
  log "Attempting to initiate IMU"

  # Recursively call the init_imu script in case it crashes
  $MISSION_ROOT/scripts/init_imu.sh $EXISTING_FILES && init_imu
}

init_imu () {
  try_init_imu
  sleep 1
}

#INIT Camera
try_init_camera () {
  log "Attempting to initiate camera"

  $MISSION_ROOT/scripts/init_camera.sh && init_camera
}

init_camera () {
  try_init_camera
  sleep 1
}

init_camera & init_imu
