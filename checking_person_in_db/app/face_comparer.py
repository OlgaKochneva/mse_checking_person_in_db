import pickle

import face_recognition
import numpy as np


class FaceComparer:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []

        self.unknown_faces_counter = 0

        self.tolerance = 0.52

    def load_encodings(self, path_to_data):
        with open(path_to_data, 'rb') as data_file:
            data = pickle.load(data_file)

        self.known_encodings = data['encodings']
        self.known_names = data['names']

    def compare(self, frame, locations):
        encodings = face_recognition.face_encodings(frame, locations)
        detected_faces = {}

        for index, encoding in enumerate(encodings):
            matches = face_recognition.compare_faces(self.known_encodings,
                                                     encoding,
                                                     tolerance=self.tolerance)

            face_distances = face_recognition.face_distance(self.known_encodings, encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_names[best_match_index]
            else:
                name = f'Unknown{self.unknown_faces_counter}'
                self.known_encodings += [encoding]
                self.known_names += [name]
                self.unknown_faces_counter += 1

            detected_faces[name] = locations[index]

        return detected_faces
