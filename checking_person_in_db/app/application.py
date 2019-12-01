import os
import re

from .face_comparer import FaceComparer
from .face_finder import FaceFinder
from .utilities import msg
from .video_handler import VideoHandler


class App:
    def __init__(self, video_source, path_to_features='../db_creator/resources/features.pkl'):
        if re.match(r'((.*\.(mp4|avi)$|\d+))', video_source) is None:
            msg('err',
                'Please, specify the file extension or provide stream id\n'
                '         Example: <path>/file.mp4 | <path>/file.avi 0,1, ...', print)
            raise SystemExit(1)

        if video_source.isdigit():
            self.video_handler = VideoHandler(int(video_source))
        else:
            self.video_handler = VideoHandler(os.path.abspath(video_source))

        self.face_finder = FaceFinder()
        self.face_comparer = FaceComparer()

        self.face_comparer.load_encodings(path_to_features)

    def run(self):
        self.face_finder.process(self.video_handler, self.face_comparer)
