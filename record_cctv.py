#!/home/victor/documents/cctv/venv/bin/python3

import cctv

vr = cctv.VideoRecorder(sizex=1280, sizey=720)
vr.record()
