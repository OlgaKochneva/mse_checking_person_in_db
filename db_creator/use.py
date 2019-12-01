import face_recognition
import cv2
import numpy as np
import pickle
import keyboard
import dlib

with open('resources/features.pkl', 'rb') as f:
    data = pickle.load(f)

known_face_encodings = data['encodings']
known_face_names = data['names']

face_locations = []
face_encodings = []
face_names = []

cap = cv2.VideoCapture('../videos/avengers.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

video_tracked = cv2.VideoWriter('../videos/result.avi',
                                fourcc,
                                int(cap.get(cv2.CAP_PROP_FPS)),
                                (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

i = 0
ret = True

while ret:
    ret, frame = cap.read()

    if i % 10 == 0 and frame is not None:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.52)

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                face_names.append(name)

            else:
                face_names.append('Unknown')

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 1
            right *= 1
            bottom *= 1
            left *= 1

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

    video_tracked.write(frame)
    i += 1

    if keyboard.is_pressed('q'):
        break

cap.release()