Video-to-Frame (Video-Based Preprocessing Pipeline)

This repository demonstrates a video-based preprocessing pipeline that converts a short full-body rotation video into a minimal set of high-quality, angularly diverse frames suitable for 3D body reconstruction.

Project Structure
video-to-good-frames/
│
├─ scripts/
│   └─ video_to_good_frames.py
│
├─ videos/
│   └─ input.mp4          # sample / test video
│
├─ good_frames/            # auto-created output folder



What This Pipeline Does
  Uses FFmpeg to sample frames from the input video
  Runs MediaPipe Pose to score pose quality
  Enforces angular diversity (front / side / back views)
  Removes near-duplicate frames
  Outputs only 4–5 high-quality frames for 3D reconstruction

Input Requirements
8–15 second video
Full body visible (head to feet)
User rotates slowly 360°
Tight-fitting clothes
Plain background
Camera fixed, person rotates

Place the video here:
videos/input.mp4

- Requirements
Python Version
Python 3.10 (64-bit)
 Do not use Python 3.12+ or 3.14 (MediaPipe is not stable)

Required Libraries (requirements.txt)
mediapipe==0.10.9
opencv-python==4.11.0.86
numpy==1.26.4


These versions are stable on Windows + Python 3.10.

-  Setup Instructions
1. Create virtual environment
python -m venv venv

Activate:
Windows
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run the pipeline
cd scripts
python video_to_good_frames.py

-- Output --
After running, the output folder will be created automatically:
good_frames/
 ├─ frame_001.jpg
 ├─ frame_002.jpg
 ├─ frame_003.jpg
 ├─ frame_004.jpg
 └─ frame_005.jpg


These frames are:
Pose-validated
Angularly diverse
Ready for 3D body reconstruction

-- Next Step
The selected frames will be passed to PARE + SMPL-X to reconstruct a 3D body model and extract accurate body measurements from the mesh.

- Summary

Video → FFmpeg → Pose filtering → Angular selection → 4–5 good frames → 3D body model
