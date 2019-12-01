from ordered_set import OrderedSet

from .utilities import format_time


class Singleton(type):
    def __call__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__call__()
        return cls.instance


class Report(metaclass=Singleton):
    def __init__(self):
        self.records = {}

    def add(self, time, new_faces, lost_faces):
        self.records[time] = {'new': new_faces, 'lost': lost_faces}

    def write(self, filepath=None):
        current_faces = set()
        face_appeartime = {}
        unknowns = set()
        records = OrderedSet()
        for time_ms, faces in self.records.items():
            new_faces = faces['new']
            lost_faces = faces['lost']

            for new_face in new_faces:
                if new_face.startswith('Unknown'):
                    unknowns.add(new_face)
                else:
                    current_faces.add(new_face)
                    face_appeartime[new_face] = time_ms

            for lost_face in lost_faces:
                if lost_face in current_faces:
                    records.add(f'{format_time(face_appeartime[lost_face])} — {format_time(time_ms)} | {lost_face}')

            current_faces -= set(lost_faces)

        with open(filepath, 'w') as report_file:
            for record in records:
                report_file.write(f'{record}\n')
            report_file.write(f'Unknowns count: {len(unknowns)}')
