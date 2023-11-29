#!/bin/bash -e
MISSION_ROOT=~/mission
cp $MISSION_ROOT/scripts/detect_system_failure /tmp/ && /tmp/detect_system_failure $MISSION_ROOT $MISSION_ROOT/scripts/log.sh
