from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
import time

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
print("Created camera")

encoder = H264Encoder(bitrate=int(2e7))
output = FfmpegOutput("test.mp4")

print("Starting recording")
picam2.start_recording(encoder, output)
for i in range(20):
    time.sleep(1)
    print(f"t={i}")
print("Stopping recording")
picam2.stop_recording()
print("Done!")
