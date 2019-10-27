import os

import cv2
import face_recognition
# import keyboard

from .utilities import msg


class FaceFinder:
    def __init__(self):
        self.processed_frames = []
        self.face_locations_per_frame = []
        self.resize_scale = 0.5

    def process(self, video_source):
        settings = video_source.settings()
        frame_count = 0

        ret, frame = video_source.read()
        while ret:
            # if keyboard.is_pressed('q'):
            #     break

            msg('progress', f'{(frame_count * 100 / settings["length"]):.1f}%', print)
            processed_frame = frame.copy()
            small_frame = cv2.resize(processed_frame, (0, 0), fx=self.resize_scale, fy=self.resize_scale)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)

            for top, right, bottom, left in face_locations:
                top *= int(1 / self.resize_scale)
                right *= int(1 / self.resize_scale)
                bottom *= int(1 / self.resize_scale)
                left *= int(1 / self.resize_scale)

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            self.face_locations_per_frame += [face_locations]

            self.processed_frames += [frame]
            frame_count += 1
            ret, frame = video_source.read()

        self.create_tracked_video(settings)

    # 1st iteration result
    def create_tracked_video(self, video_info):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_tracked = cv2.VideoWriter(f'{os.path.abspath("../resources/result.avi")}',
                                        fourcc,
                                        video_info['fps'],
                                        (video_info['width'], video_info['height']))
        for frame in self.processed_frames:
            video_tracked.write(frame)
        video_tracked.release()
        print('\nresult.avi created')
