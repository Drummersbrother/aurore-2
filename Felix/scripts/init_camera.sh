MISSION_ROOT=~/mission

log () {
  $MISSION_ROOT/scripts/log.sh "$1"
}

cd $MISSION_ROOT/camera-footage
EXISTING_VIDEOS=$(ls -1q video* | wc -l)
OUTPUT_NAME="$MISSION_ROOT/camera-footage/video$EXISTING_VIDEOS.mp4"

cd $MISSION_ROOT/scripts
python3 $MISSION_ROOT/scripts/run_camera.py $OUTPUT_NAME
if [ $? != 0 ]; then
  log "Camera Python script crashed"
fi
