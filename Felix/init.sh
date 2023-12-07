#!/bin/bash -e
VERBOSE=true
# User must be explicitly specified, because systemctl service is run with USER=root
USER=$1
MISSION_ROOT=/home/$USER/mission


# Ensure the existance of the "logs" directory
mkdir -p $MISSION_ROOT/logs;

# Ensure the existance of the "imu-reports" directory
mkdir -p $MISSION_ROOT/imu-reports

# Ensure the existance of the "camera-footage" directory
mkdir -p $MISSION_ROOT/camera-footage


# INIT LOG
# Create new log file
EXISTING_FILES=$(ls -1q $MISSION_ROOT/logs/log* | wc -l)
LOG_FILE="log$EXISTING_FILES"
touch $MISSION_ROOT/logs/$LOG_FILE

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

# Function to log message to the master log file for this session
log () {
  $MISSION_ROOT/scripts/log.sh "$1"
}

#INIT IMU
try_init_imu() {
  log "Attempting to initiate IMU"

  # Recursively call the init_imu script in case it crashes
  $MISSION_ROOT/scripts/init_imu.sh $USER $EXISTING_FILES && init_imu
}

init_imu () {
  sleep 1
  try_init_imu
}

#INIT Camera
try_init_camera () {
  log "Attempting to initiate camera"

  $MISSION_ROOT/scripts/init_camera.sh $USER && init_camera
}

init_camera () {
  sleep 1
  try_init_camera
}

#INIT OLED
try_init_oled () {
  log "Attempting to initiate OLED screen"

  $MISSION_ROOT/scripts/init_oled.sh $USER && init_oled
}

init_oled () {
  sleep 1
  try_init_oled
}

init_camera & init_imu & init_oled
