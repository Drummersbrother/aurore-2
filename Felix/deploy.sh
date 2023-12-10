#!/bin/bash -e
set -euxo pipefail
MISSION_USERNAME=felixhellborg
MISSION_HOSTNAME=aurore2.local
TRANSFER_CMD="rsync --progress"
ssh $MISSION_USERNAME@$MISSION_HOSTNAME mkdir -p mission

$TRANSFER_CMD -r init.sh $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/

$TRANSFER_CMD -r scripts $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/

if [ "$1" != "--no-build" ]; then
  (cd detect-system-failure || exit 1;
    cross build --release --target aarch64-unknown-linux-gnu
    $TRANSFER_CMD -r ./target/aarch64-unknown-linux-gnu/release/detect-system-failure $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/scripts/detect_system_failure  
  )
fi

$TRANSFER_CMD -r media $MISSION_USERNAME@$MISSION_HOSTNAME:~/mission/

$TRANSFER_CMD reboot-watchdog-init/* $MISSION_USERNAME@$MISSION_HOSTNAME:~/

if [ "$2" != "--no-ssh" ]; then
  ssh $MISSION_USERNAME@$MISSION_HOSTNAME
fi
