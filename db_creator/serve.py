import os

path_to_train_dir = 'resources/train'

for path_to_person_dir in os.listdir(path_to_train_dir):

    """try:
        i = path_to_person_dir.index(' ')

        new_path_to_person_dir = path_to_person_dir[:i] + '_' + path_to_person_dir[i + 1:].capitalize()

        os.rename(path_to_train_dir + '/' + path_to_person_dir, path_to_train_dir + '/' + new_path_to_person_dir)

    except:
        pass"""

    path_to_person_dir = os.path.join(path_to_train_dir, path_to_person_dir)

    for path_to_person_img in os.listdir(path_to_person_dir)[15:]:
        os.remove(path_to_person_dir + '/' + path_to_person_img)