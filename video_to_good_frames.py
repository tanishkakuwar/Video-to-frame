import cv2
import mediapipe as mp
import subprocess
import numpy as np
import os
import math

# ---------------- CONFIG ----------------
VIDEO_PATH = "../videos/input.mp4"
OUTPUT_DIR = "../good_frames"

TARGET_FPS = 5
FINAL_FRAMES = 5        # set to 4 or 5
SEGMENTS = 4            # front / side / back / side
MIN_FRAME_GAP = 3       # prevents frames too close in time
# ----------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

# FFmpeg → raw frames in memory
cmd = [
    "ffmpeg",
    "-i", VIDEO_PATH,
    "-vf", f"fps={TARGET_FPS}",
    "-f", "image2pipe",
    "-pix_fmt", "bgr24",
    "-vcodec", "rawvideo",
    "-"
]

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

# Get video resolution
cap = cv2.VideoCapture(VIDEO_PATH)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()

FRAME_SIZE = W * H * 3

all_frames = []
frame_idx = 0

# -------- Frame ingestion + pose scoring --------
while True:
    raw = process.stdout.read(FRAME_SIZE)
    if len(raw) < FRAME_SIZE:
        break

    frame = np.frombuffer(raw, np.uint8).reshape((H, W, 3))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = pose.process(rgb)
    if result.pose_landmarks:
        vis = [lm.visibility for lm in result.pose_landmarks.landmark]
        confidence = sum(vis) / len(vis)
        all_frames.append((frame_idx, frame.copy(), confidence))

    frame_idx += 1

# -------- Angular diversity (time-based) --------
segment_size = math.ceil(len(all_frames) / SEGMENTS)
selected = []

for i in range(SEGMENTS):
    start = i * segment_size
    end = start + segment_size
    segment = all_frames[start:end]

    segment.sort(key=lambda x: x[2], reverse=True)

    for candidate in segment:
        if all(abs(candidate[0] - s[0]) >= MIN_FRAME_GAP for s in selected):
            selected.append(candidate)
            break

# -------- Optional extra best frame --------
if FINAL_FRAMES == 5:
    all_frames.sort(key=lambda x: x[2], reverse=True)
    for candidate in all_frames:
        if all(abs(candidate[0] - s[0]) >= MIN_FRAME_GAP for s in selected):
            selected.append(candidate)
            break

# -------- Save output (ordered) --------
selected = selected[:FINAL_FRAMES]

for i, (_, frame, _) in enumerate(selected):
    out_path = os.path.join(OUTPUT_DIR, f"frame_{i+1:03d}.jpg")
    cv2.imwrite(out_path, frame)

print(f"Saved {len(selected)} final frames to good_frames/")
