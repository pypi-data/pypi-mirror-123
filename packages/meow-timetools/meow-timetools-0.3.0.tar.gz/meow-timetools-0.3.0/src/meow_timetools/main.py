import argparse
import os.path
import time
import json
from datetime import datetime

from cv2.cv2 import VideoCapture, imwrite


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", default=".", help="Folder to store images in")
    parser.add_argument("--annotation", default="annotations.json", help=".json to store annotations in")
    parser.add_argument("--camera", "-c", default=0, help="cam")
    args = parser.parse_args([] if "__file__" not in globals() else None)
    return args


def capture(camera_id, path):

    if not os.path.isdir(path):
        os.makedirs(path)

    path = os.path.join(path, datetime.now().strftime("%m_%d_%Y %H:%M:%S") + ".png")

    cam = VideoCapture(camera_id)
    s, img = cam.read()
    if s:
        imwrite(path, img)


def capture_image():
    args = get_args()
    capture(args.camera, args.images)


def annotate_images():
    args = get_args()


def start_timer():
    args = get_args()

    while True:
        capture(args.camera, args.images)
        time.sleep(60 * 10)


if __name__ == "__main__":
    print("Use pip to start this app")
