#!/bin/bash -e
USER=$1
MISSION_ROOT=/home/$USER/mission

log () {
  $MISSION_ROOT/scripts/log.sh "$1"
}

# Try to find the oled module. Should be on 3c
if [[ $(i2cdetect -y 1 | grep -o "3c") == "3c" ]]; then
  log "Found OLED module at address 3c"

  python3 $MISSION_ROOT/scripts/run_oled.py
  
  if [ $? != 0 ]; then
    log "OLED Python script crashed"
  fi
else
  log "Could not find any I2C devices at address 3c"
fi
