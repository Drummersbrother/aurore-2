from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
import time

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
print("Created camera")

encoder = MJPEGEncoder(bitrate=int(5e7))
output = FfmpegOutput("test.mp4")

print("Starting recording")
picam2.start_recording(encoder, output)
time.sleep(10)
print("Stopping recording")
picam2.stop_recording()
print("Done!")
