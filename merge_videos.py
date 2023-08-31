import os
import yaml
import numpy as np
import cv2
import imageio

def get_video(vid_in, size=None):
    # define a video capture object
    cap = cv2.VideoCapture(vid_in)
    width  = int(cap.get(3))  # float `width`
    height = int(cap.get(4))  # float `height`
    
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    
    frames = []
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            if size is not None:
                frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
            frames.append(frame)
        else: 
            break
  
    # After the loop release the cap object
    cap.release()

    return frames

with open("prompts.yaml", "r") as f:
    prompts = yaml.safe_load(f)
    keys = sorted(prompts.keys())

content = ""
page_idx = 0
prev_i = 0
page_size = 5
for i,k in enumerate(keys):
    all_frames = []
    for m in ["dreamfusion-if", "magic3d-refine-sd", "textmesh-if", "prolificdreamer", "ours"]:
        video_file = f"static/results/{m}/{k}/demo.mp4"
        frames = get_video(video_file, (320,320))
        all_frames.append(frames)
    
    all_frames = [np.concatenate(frames, axis=1) for frames in zip(*all_frames)]
    all_frames = [f[:,:,::-1] for f in all_frames]
    imageio.mimwrite(f"static/merged_results_320/{k}.mp4", all_frames, fps=30)
    print(f"static/merged_results_320/{k}.mp4")