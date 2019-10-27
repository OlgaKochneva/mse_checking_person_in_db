"""
You need to prepare .json
to execute this script.
It must contain test suit.
The very necessary parameters of
test suit are .avi and .csv.
So if you haven't prepared them,
go to ./tests/test_generator/video_test_generator.py
and generate them.
The script tests
    1) correct behavior of the program
    if it accepts an invalid format file
    (expected correct shutdown
    without video processing);
    2) correct behavior of the program
    if it accepts file which doesn't exist
    (expected correct shutdown
    without video processing);
    3) the quality of scanning faces
    in the frame (one parameter of
    test case is the quality threshold).
Use py.test -v test.py command
to execute this script.
"""
import sys

sys.path.append('../')

from checking_person_in_db.app import *
import pytest
import csv
from json import load

with open('test_suit.json', 'r') as f:
    test_suit = load(f)


@pytest.mark.parametrize('command_line_argument', test_suit['badFileFormatTest'])
def test_inadmissibility_inappropriate_file_format(command_line_argument):
    with pytest.raises(SystemExit):
        App(command_line_argument).run()


@pytest.mark.parametrize('command_line_argument', test_suit['videoExistenceTest'])
def test_video_stream_existance(command_line_argument):
    with pytest.raises(SystemExit):
        App(command_line_argument).run()


@pytest.mark.parametrize('video_data_threshold', test_suit['properFaceFindingTest'])
def test_proper_face_finding(video_data_threshold):
    def is_face_inside(right_location, face_location):
        x0_, w0_, y0_, h0_ = right_location
        top, right, bottom, left = face_location

        return x0_ <= left and y0_ <= top and x0_ + w0_ <= right and y0_ + h0_ <= bottom

    testing_video, path_to_dataset, threshold = video_data_threshold

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

    f.close()
    assert quality > threshold
