import _pickle
import os
import face_recognition

from app.model import Persons


def init_database(path_to_train_dir='../resources/train/'):  # change path
    train_dir = os.listdir(path_to_train_dir)
    count_persons = len(train_dir)
    person_counter = 0
    train_dir = os.listdir(path_to_train_dir)
    print(f'\r0/{count_persons} of people have been processed (0.0%).', end='')

    for path_to_person_dir in train_dir:
        paths_to_person_imgs = os.listdir(path_to_train_dir + path_to_person_dir)
        encodings = []
        for path_to_person_img in paths_to_person_imgs:
            face = face_recognition.load_image_file(
                path_to_train_dir + path_to_person_dir + '/' + path_to_person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                encodings.append(face_enc)

        person = Persons(name=path_to_person_dir, face_encodings=_pickle.dumps(encodings, protocol=2))
        person.save()

        person_counter += 1
        print(f'\r{person_counter}/{count_persons} '
              f'of people have been processed ({person_counter / count_persons * 100: .0f}%).', end='')


if __name__ == '__main__':
    init_database()
