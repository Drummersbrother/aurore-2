import sys
import os

H = 64
W = 128


def convert_videos():
    from PIL import Image, ImageSequence
    import cv2
    import numpy as np
    import tqdm
    import glob

    video_folder_path = "Hugo/source_videos/*"
    out_folder_path = "Hugo/processed_videos/"
    video_files = glob.glob(video_folder_path)

    video_converted = {}
    for vid_inx, video_file in enumerate(video_files):
        cap = cv2.VideoCapture(video_file)

        frame_inx = 0
        frames = []
        vid_pbar = tqdm.tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), desc=f"Converting {video_file}")
        while cap.isOpened():
            ret, frame = cap.read()
            if ret == False:
                break
            resized_frame = cv2.resize(frame, (W, H), interpolation=cv2.INTER_AREA)
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            (thresh, resized_frame) = cv2.threshold(resized_frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            frames.append(resized_frame)
            frame_inx += 1
            vid_pbar.update(1)

        video_converted[video_file] = np.stack(frames)
        print(video_converted[video_file].shape)
        # Save numpy array
        np.save(out_folder_path + f"video_{vid_inx}.npy", video_converted[video_file])

        cap.release()


def export_previews():
    # Export previews
    # Convert to viewable videos, from the numpy arrays
    import numpy as np
    import glob
    import tqdm
    import time
    import cv2

    video_folder_path = "Hugo/processed_videos/*"
    video_files = glob.glob(video_folder_path)

    out_folder_path = "Hugo/preview_videos/"
    # Convert to uncompressed videos
    for video_path in video_files:
        print(f"Exporting preview of {video_path}")
        vid_data = np.load(video_path)
        vid_inx = os.path.basename(video_path).split("_")[-1].split(".")[0]
        size = H, W
        fps = 30
        out = cv2.VideoWriter(os.path.join(out_folder_path, f"vid_{vid_inx}.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), fps, (size[1], size[0]), False)
        for frame in vid_data:
            out.write(frame)
        out.release()


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "convert":
        convert_videos()
    elif len(sys.argv) >= 2 and sys.argv[1] == "export":
        export_previews()
    elif len(sys.argv) >= 2 and sys.argv[1] == "both":
        convert_videos()
        export_previews()
    else:
        print("Usage: python3 Hugo/convert_videos.py [convert|export|both]")
