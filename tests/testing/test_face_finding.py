import sys
import pytest
import csv
from json import load
from subprocess import call
from os import chdir

from checking_person_in_db.app import *
from tests.checking_utilities import *

sys.path.append('../../')

chdir('../test_generators')
call(['python', 'finding_face_test_generator.py'])   # main process waits until subprocess completes
chdir('../testing')


with open('test_suit.json', 'r') as f:
    test_suit = load(f)


@pytest.mark.parametrize('finding_face_data_threshold', test_suit['properFaceFindingTest'])
def test_proper_face_finding(finding_face_data_threshold):
    testing_video, path_to_dataset, threshold = finding_face_data_threshold

    f = open(path_to_dataset)

    csv_reader = csv.reader(f, delimiter=',')
    next(csv_reader)

    app = App(testing_video)
    app.run()

    face_locations_per_frame = app.face_finder.face_locations_per_frame

    quality = 0
    for face_locations in face_locations_per_frame:
        right_locations = list(map(int, next(csv_reader)[1:]))
        right_location_0, right_location_1 = right_locations[:4], right_locations[4:]
        len_face_locations = len(face_locations)

        if right_location_0[0] < 0:
            if len_face_locations > 0:
                quality -= len_face_locations
        else:
            if any(x is True for x in list(map(lambda x: is_face_inside(x, right_location_0), face_locations))):
                quality += 1

            if right_location_1 and \
                    any(x is True for x in list(map(lambda x: is_face_inside(x, right_location_1), face_locations))):
                quality += 1

            elif not right_location_1 and len_face_locations > 1:
                quality -= 1

            if len_face_locations > 2:
                quality -= (len_face_locations - 2)

        for i in range(app.face_finder.skip_frames_num - 1):
            next(csv_reader)

    f.close()

    assert quality >= threshold