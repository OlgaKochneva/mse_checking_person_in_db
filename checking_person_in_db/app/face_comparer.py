import _pickle
import heapq

import face_recognition
import numpy as np
import recordclass

from .model import Persons

CachedPerson = recordclass.make_dataclass('CachedPerson', ['name', 'face_encodings'])


class FaceComparer:
    def __init__(self):
        self.unknown_faces_counter = 0
        self.tolerance = 0.55
        self.persons_database = Persons.objects
        self._persons_cached = set()

    def _compare_persons(self, face_data, encoding):
        names = []
        for person in face_data:
            face_distances = face_recognition.face_distance(_pickle.loads(person.face_encodings), encoding)
            min_dist = np.amin(face_distances)
            if True in list(face_distances <= self.tolerance):
                heapq.heappush(names, (min_dist, person.name))
                self._persons_cached.add(CachedPerson(person.name, person.face_encodings))

        if len(names) > 0:
            name = heapq.heappop(names)[1]
        else:
            name = None

        return name

    def compare(self, frame, locations):
        encodings = face_recognition.face_encodings(frame, locations)
        detected_faces = {}

        for index, encoding in enumerate(encodings):
            name = self._compare_persons(self._persons_cached, encoding)
            if name is None:
                name = self._compare_persons(self.persons_database, encoding)

            if name is None:
                name = f'Unknown{self.unknown_faces_counter}'
                self._persons_cached.add(CachedPerson(name=name, face_encodings=_pickle.dumps([encoding])))
                self.unknown_faces_counter += 1

            detected_faces[name] = locations[index]

        return detected_faces
