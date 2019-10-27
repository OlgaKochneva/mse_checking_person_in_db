import sys
import cv2

from .utilities import msg


class VideoHandler:
    def __init__(self, video_source):
        self.cap = cv2.VideoCapture(video_source)

        if not self.cap.isOpened():
            msg('err', f'Invalid video stream {video_source}', print)
            raise SystemExit(1)

        self.info = {
            'fps': int(self.cap.get(cv2.CAP_PROP_FPS)),
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'length': int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        }

    def read(self):
        return self.cap.read()

    def settings(self):
        return self.info

    def __del__(self):
        self.cap.release()
