import os
import sys
from time import time

import cv2
import face_recognition
import keyboard

from .report import Report
from .utilities import msg, handle_faces_presence, spinning_cursor


class FaceFinder:
    def __init__(self):
        self.face_locations_per_frame = []
        self.resize_scale = 0.5
        self.skip_frames_num = 5
        self.upsample_num = 1

    def process(self, video_source, face_comparer):
        settings = video_source.settings()
        frame_count = 0

        tracked_video = self.create_tracked_video(settings)
        ret, frame = video_source.read()
        is_stream = settings['length'] <= 0
        start_time = time()
        prev_frame_faces = []
        report = Report()
        spinner = spinning_cursor()
        while ret:
            if keyboard.is_pressed('q'):
                break

            if frame_count % self.skip_frames_num == 0:
                if not is_stream:
                    msg('progress', f'{(frame_count * 100 / settings["length"]):.1f}%', sys.stdout.write)
                else:
                    msg('progress', f'{next(spinner)}', sys.stdout.write)
                sys.stdout.write('\r')

                processed_frame = frame.copy()
                small_frame = cv2.resize(processed_frame, (0, 0), fx=self.resize_scale, fy=self.resize_scale)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame,
                                                                 number_of_times_to_upsample=self.upsample_num)
                detected_faces = face_comparer.compare(rgb_small_frame, face_locations)

                current_msec = video_source.cap.get(cv2.CAP_PROP_POS_MSEC) if not is_stream \
                    else (time() - start_time) * 1000
                report.add(current_msec, *handle_faces_presence(prev_frame_faces, detected_faces))
                prev_frame_faces = detected_faces

                for name, location in detected_faces.items():
                    top, right, bottom, left = location
                    top *= int(1 / self.resize_scale)
                    right *= int(1 / self.resize_scale)
                    bottom *= int(1 / self.resize_scale)
                    left *= int(1 / self.resize_scale)
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)

                self.face_locations_per_frame += [face_locations]

                # later report update instead of write
                tracked_video.write(frame)

            frame_count += 1
            ret, frame = video_source.read()
        msg('progress', 'result.avi created', print)
        tracked_video.release()

        report.write(os.path.abspath('../resources/report.txt'))
        msg('progress', 'report.txt created', print)

    # 1st iteration result
    def create_tracked_video(self, video_info):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = video_info['fps'] // self.skip_frames_num
        video_tracked = cv2.VideoWriter(f'{os.path.abspath("../videos/result.avi")}',
                                        fourcc,
                                        fps if video_info["length"] != -1 else fps // 3,
                                        (video_info['width'], video_info['height']))
        return video_tracked
