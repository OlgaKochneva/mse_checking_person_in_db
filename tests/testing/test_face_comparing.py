import sys
import cv2
import face_recognition
import pytest
import csv
from json import load
from os import chdir
from subprocess import call

from checking_person_in_db.app import *
from tests.checking_utilities import *

path_to_features = '../../db_creator/resources/features.pkl'

sys.path.append('../../')

chdir('../test_generators')
call(['python', 'compare_test_generator.py'])  # main process waits until subprocess completes
chdir('../testing')


with open('test_suit.json', 'r') as f:
    test_suit = load(f)


@pytest.mark.parametrize('compare_data_threshold', test_suit['properFaceComparingTest'])
def test_proper_face_comparing(compare_data_threshold):
    testing_img, path_to_dataset, threshold = compare_data_threshold

    face_comparer = FaceComparer()
    face_comparer.load_encodings(path_to_features)

    f = open(path_to_dataset)
    csv_reader = csv.reader(f, delimiter=',')
    next(csv_reader)  # skip header

    correct_data = {}
    for row in csv_reader:
        correct_data[row[0]] = list(map(int, row[1:]))

    img = cv2.imread(testing_img)

    locations = face_recognition.face_locations(img, number_of_times_to_upsample=2)
    result = face_comparer.compare(img, locations)

    # sort names to match them
    # possible because test data doesn't contain duplicate faces
    result_names = sorted(result)
    sorted_names = sorted(correct_data)

    quality = 0

    for i, name in enumerate(result_names):
        correct_name = sorted_names[i]
        if name == 'Unknown':
            quality -= len(result)
        else:
            # check if name is correct and in the right place
            if name == correct_name and is_face_inside(result[name], correct_data[correct_name]):
                quality += 1
            else:
                quality -= 1

    assert quality >= threshold
