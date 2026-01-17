# Video-to-frame
This repo demonstrates a video-based preprocessing pipeline that selects a minimal set of high-quality, diverse frames for 3D body reconstruction.

video-to-good-frames/
│
├─ scripts/
│   └─ video_to_good_frames.py
│
├─ videos/
│   └─ input.mp4          # sample / test video
│
├─ good_frames/            # auto-created
│
├─ requirements.txt


- Required Libraries (requirements.txt)
    Create a file called requirements.txt
    mediapipe==0.10.9
    opencv-python==4.11.0.86
    numpy==1.26.4

   These versions are stable on Windows + Python 3.10

Input Requirements
- 8–15 sec video
- Full body visible
- User rotates slowly 360°
- Tight clothes
- Plain background
- Camera fixed, person rotates


- Setup Instructions
    1. Install Python (required)
         Use **Python 3.10 (64-bit)**  
         Do not use Python 3.12+ or 3.14 (MediaPipe not stable)

    2. Create virtual environment
   ```bash
      python -m venv venv

-Install dependencies
    pip install -r requirements.txt

-cd scripts
    python video_to_good_frames.py


Next, I’ll feed these frames into PARE + SMPL-X to reconstruct a 3D body model and extract accurate body measurements from the mesh
