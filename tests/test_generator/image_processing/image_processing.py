import cv2
import random


def get_random_fg_place(y_range, x_range):
    return random.randint(*y_range), random.randint(*x_range)


def reduce_img_randomly(img, scale_factor_range=(1, 1)):
    scale_factor = random.uniform(*scale_factor_range)

    new_img_dim = tuple(reversed(list(map(lambda x: int(x * scale_factor), img.shape[:2]))))
    img = cv2.resize(img, new_img_dim, cv2.INTER_AREA)
    return img


def add_fg_on_bg(fg, bg, place, black_color_threshold=0):
    x, y = place
    fg_h, fg_w = fg.shape[:2]

    fg_gray = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)

    bg_part_for_fg = bg[y: y + fg_h, x: x + fg_w]

    ret, mask = cv2.threshold(fg_gray, black_color_threshold, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(bg_part_for_fg, bg_part_for_fg, mask=mask_inv)
    img2_fg = cv2.bitwise_and(fg, fg, mask=mask)
    dst = cv2.add(img1_bg, img2_fg)
    bg[y: y + fg_h, x: x + fg_w] = dst

    return bg