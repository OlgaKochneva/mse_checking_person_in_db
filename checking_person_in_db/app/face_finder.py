import os
import sys
from datetime import datetime
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
        self.generate_video = False
        self.generate_report = False

    def process(self, video_source, face_comparer):
        settings = video_source.settings()
        frame_count = 0
        timestamp = str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        if self.generate_video:
            tracked_video = self.create_tracked_video(settings, timestamp)
        if self.generate_report:
            report = Report()
        ret, frame = video_source.read()
        is_stream = settings['length'] <= 0
        start_time = time()
        prev_frame_faces = []
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
                if self.generate_video:
                    tracked_video.write(frame)
                if self.generate_report:
                    report.add(current_msec, *handle_faces_presence(prev_frame_faces, detected_faces))
                prev_frame_faces = detected_faces

            frame_count += 1
            ret, frame = video_source.read()

        if self.generate_video:
            tracked_video.release()
            msg('progress', f'video_{timestamp}.mp4 created', print)
        if self.generate_report:
            # generating report at same dir independently from exec point
            path_dir = os.path.abspath(os.path.dirname(__file__))
            report.write(f'{path_dir}/../out/report_{timestamp}.txt')
            msg('progress', f'report_{timestamp}.txt created', print)

    def create_tracked_video(self, video_info, timestamp):
        # generating video at same dir independently from exec point
        path_dir = os.path.abspath(os.path.dirname(__file__))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        fps = video_info['fps'] // self.skip_frames_num if self.skip_frames_num > 0 else video_info['fps']
        video_tracked = cv2.VideoWriter(f'{path_dir}/../out/video_{timestamp}.mp4',
                                        fourcc,
                                        fps if video_info["length"] != -1 else fps // 4,
                                        (video_info['width'], video_info['height']))
        return video_tracked
