from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
import time
import sys
import os

def log(message: str):
    os.system("~/mission/scripts/log.sh \"%s\"" % message)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration())

encoder = H264Encoder(bitrate=int(2e7))
output_name = sys.argv[1]
output = FfmpegOutput(output_name)

log("Starting recording")
picam2.start_recording(encoder, output)
time.sleep(5)
log("Stopping recording")
picam2.stop_recording()
