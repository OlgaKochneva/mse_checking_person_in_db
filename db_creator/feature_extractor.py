import face_recognition
import os
import time
import pickle

path_to_train_dir = 'resources/train/'
path_to_features = 'resources/features.pkl'

train_dir = os.listdir(path_to_train_dir)
count_persons = len(train_dir)
start_time = time.time()
encodings = []
names = []
person_counter = 0

print(f'\r0/{count_persons} of people have been processed (0.0%).', end='')
for path_to_person_dir in train_dir:
    paths_to_person_imgs = os.listdir(path_to_train_dir + path_to_person_dir)

    for path_to_person_img in paths_to_person_imgs:
        face = face_recognition.load_image_file(path_to_train_dir + path_to_person_dir + '/' + path_to_person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            encodings.append(face_enc)
            names.append(path_to_person_dir)

    person_counter += 1
    print(f'\r{person_counter}/{count_persons} '
          f'of people have been processed ({person_counter / count_persons * 100: .0f}%).', end='')

print(f'\nTime elapsed: {(time.time() - start_time) / 60: .1f} min.')

data = {'encodings': encodings, 'names': names}

with open(path_to_features, 'wb') as f:
    pickle.dump(data, f)

