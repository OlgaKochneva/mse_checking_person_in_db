"""
You need to prepare image for
background and images that contain
people on black context or transparent
background if the image is .png
to execute this script.
The opencv library ignores alpha channel
if the cv2.IMREAD_COLOR flag is set.
So the transparent background changes to
black context. Images that contain people
must be smaller than the image for
background. This applies to both
image height and width.
The script generates .avi and .csv.
The procedure which will be described
bellow is performed for each frame.
It is chosen randomly if people
will be put in frame. If it's true,
it's chosen the first person randomly
and put him/her in frame in random place.
Then it is chosen if the second person
will be put in frame provided that there is
enough space for him/her.
The .csv will contain the approximate
position of faces in frame or information
about their lack.
"""

import os
import cv2
import random
import csv

from image_processing.image_processing import *

if __name__ == '__main__':
    path_dir = os.path.abspath(os.path.dirname(__file__))
    path_to_imgs_people = f'{path_dir}/resources/img_people'
    bg = cv2.imread(f'{path_dir}/resources/bgs/2.jpg')
    f = open(f'{path_dir}/../finding_face_testing_dataset.csv', 'w', newline='')
    img_human_scale_factor_range = 0.7, 1
    black_color_threshold = 2
    frame_count = 100
    fps = 2

    video_writer = cv2.VideoWriter(f'{path_dir}/../finding_face_testing.avi',
                                            cv2.VideoWriter_fourcc(*'XVID'),
                                            fps,
                                    bg.T.shape[1:])

    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(['frame', 'locations'])

    people_dict = dict(enumerate(os.listdir(path_to_imgs_people)))
    people_count = len(os.listdir(path_to_imgs_people))
    people_random_list = [i for i in range(people_count)]

    for frame_counter in range(frame_count):
        frame = bg.copy()
        x0, w0, y0, h0, x1, w1, y1, h1 = [-1] * 8

        if random.randint(0, 1):
            random.shuffle(people_random_list)
            path_to_img_human = people_dict[people_random_list[0]]
            img_human = cv2.imread(os.path.join(path_to_imgs_people, path_to_img_human))

            img_human = reduce_img_randomly(img_human, img_human_scale_factor_range)

            x_range = 0, frame.shape[1] - img_human.shape[1]
            y_range = 0, frame.shape[0] - img_human.shape[0]

            y0, x0 = get_random_fg_place(y_range, x_range)

            add_fg_on_bg(img_human, frame, (x0, y0), black_color_threshold)

            if random.randint(0, 1):
                path_to_img_human_1 = people_dict[people_random_list[1]]
                img_human_1 = cv2.imread(os.path.join(path_to_imgs_people, path_to_img_human_1))

                img_human_1 = reduce_img_randomly(img_human_1, img_human_scale_factor_range)

                x_edges = x0, x0 + img_human.shape[1]

                y_range, x_range = None, None

                if x_edges[0] > img_human_1.shape[0]:
                    x_range = 0, x_edges[0] - img_human_1.shape[1]
                    y_range = 0, frame.shape[0] - img_human_1.shape[0]

                if x_range is not None:
                    y1, x1 = get_random_fg_place(y_range, x_range)

                    add_fg_on_bg(img_human_1, frame, (x1, y1), black_color_threshold)

        if x0 > 0:
            x0, w0 = x0 + img_human.shape[1] // 4, img_human.shape[1] // 2
            y0, h0 = y0, img_human.shape[1] // 2
            #cv2.rectangle(frame, (x0, y0), (x0 + w0, y0 + h0), (255, 0, 0), 2)

        if x1 > 0:
            x1, w1 = x1 + img_human_1.shape[1] // 4, img_human_1.shape[1] // 2
            y1, h1 = y1, img_human_1.shape[1] // 2
            #cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)

        csv_writer.writerow([frame_counter, x0, w0, y0, h0, x1, w1, y1, h1])
        video_writer.write(frame)

    video_writer.release()
    f.close()
