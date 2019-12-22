import cv2
import os
import random
import csv

from image_processing.image_processing import *

if __name__ == '__main__':
    path_dir = os.path.abspath(os.path.dirname(__file__))
    path_to_compare_people = f'{path_dir}/resources/compare_people'
    bg = cv2.imread(f'{path_dir}/resources/bgs/2.jpg')

    f = open(f'{path_dir}/../compare_testing_dataset.csv', 'w', newline='')

    img_human_scale_factor_range = 0.7, 1
    black_color_threshold = 2
    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(['name', 'location'])
    names = ['Mark_Ruffalo', 'Morgan_Freeman', 'Gal_Gadot', 'Bryan_Cranston']
    random.shuffle(names)

    pic = bg.copy()
    start_x, start_y, end_x, end_y = (0, 0, pic.shape[1]//2, pic.shape[0]//2)
    for i, name in enumerate(names):
        face_pic = cv2.imread(os.path.join(path_to_compare_people, f'{name}.jpg'))

        img_human = reduce_img_randomly(face_pic, img_human_scale_factor_range)

        x_range = start_x, end_x - img_human.shape[1]
        y_range = start_y, end_y - img_human.shape[0]

        start_x += pic.shape[1] // 2
        end_x += pic.shape[1] // 2

        if (i+1) % 2 == 0:
            start_x = 0
            end_x = pic.shape[1] // 2
            start_y += pic.shape[0] // 2
            end_y += pic.shape[0] // 2

        y0, x0 = get_random_fg_place(y_range, x_range)

        add_fg_on_bg(img_human, pic, (x0, y0), black_color_threshold)

        w0 = img_human.shape[1]
        h0 = img_human.shape[1]

        csv_writer.writerow([name, x0, w0, y0, h0])
        cv2.imwrite(f'{path_dir}/../compare_test_image.jpg', pic)