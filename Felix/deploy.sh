#!/bin/bash -e
set -euxo pipefail
MISSION_USERNAME=felixhellborg
MISSION_HOSTNAME=aurore2.local
ssh $MISSION_USERNAME@$MISSION_HOSTNAME mkdir -p mission

scp -r init.sh $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/

scp -r scripts $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/

(cd detect-system-failure || exit 1;
  cross build --release --target aarch64-unknown-linux-gnu
  scp -r ./target/aarch64-unknown-linux-gnu/release/detect-system-failure $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/scripts/detect_system_failure  
)

(cd register-launch || exit 1;
  cross build --release --target aarch64-unknown-linux-gnu
  scp -r ./target/aarch64-unknown-linux-gnu/release/register-launch $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/scripts/register-launch) 

scp -r media $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/

scp reboot-watchdog-init/* $MISSION_USERNAME@$MISSION_HOSTNAME:~/

ssh $MISSION_USERNAME@$MISSION_HOSTNAME 
