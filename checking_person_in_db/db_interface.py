import _pickle
import glob
import os
import re
from multiprocessing import Pool, Lock, Value, cpu_count
import click

import click
import face_recognition
from app.model import Persons


def init_process(count_persons_init, person_counter_init, lock_init):
    global INSERT_MANY
    INSERT_MANY = True
    global count_persons
    count_persons = count_persons_init
    global person_counter
    person_counter = person_counter_init  # uint
    global lock
    lock = lock_init


def insert_many_persons(path_to_train_dir):  # change path
    train_dir = os.listdir(path_to_train_dir)
    count_persons = len(train_dir)
    tasks = [(path_to_person_dir, path_to_train_dir + '/' + path_to_person_dir) for path_to_person_dir in train_dir]

    print(f'0/{count_persons} of people have been processed (0%)')
    with Pool(processes=cpu_count(), initializer=init_process, initargs=(count_persons, Value('I', 0), Lock())) as pool:
        pool.starmap(insert_one_person, tasks)
        
    pool.close()



def insert_one_person(name, path_to_person_dir):
    if not os.path.exists(path_to_person_dir) or not os.path.isdir(path_to_person_dir):
        print(f'No such file or directory: {path_to_person_dir}')
        return

    pattern = '|'.join(['.jpg', '.png'])
    paths_to_person_imgs = glob.glob(f'{path_to_person_dir}/*[{pattern}]')
    paths_to_person_imgs = list(filter(lambda path: not os.path.isdir(path), paths_to_person_imgs))

    if not paths_to_person_imgs:
        print(f'{path_to_person_dir} doesn\'t contain images with supported formats: .jpg, .png')
        return

    persons = Persons.objects(name=name)
    encodings = _pickle.loads(persons[0].face_encodings) if persons else []

    for path_to_person_img in paths_to_person_imgs:
        face = face_recognition.load_image_file(path_to_person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            encodings.append(face_enc)

    person = Persons(name=name, face_encodings=_pickle.dumps(encodings, protocol=2))

    if INSERT_MANY:
        lock.acquire()
        person.save()
        person_counter.value += 1
        print(f'{person_counter.value}/{count_persons} '
              f'of people have been processed ({person_counter.value / count_persons * 100:.0f}%) ', end='')
        lock.release()
    else:
        person.save()

    print(f'{name} successfully added')


def delete_person(name=''):
    regex = re.compile('.*' + name)
    person = Persons.objects(name=regex)
    if person:
        person.delete()
        print(f'All {name} data was deleted')
    else:
        print('No such person in db')


def show_persons():
    names = [person.name for person in Persons.objects]
    if names:
        for name in sorted(names):
            print(name)
    else:
        print("No persons in db")


def get_name(ctx, param, is_needed):
    if is_needed:
        name = ctx.params.get('name')
        if not name:
            name = click.prompt('Name')
        return name


def get_path(ctx, param, is_needed):
    if is_needed:
        path = ctx.params.get('path')
        if not path:
            path = click.prompt('Path')
        return path


def get_all(ctx, param, is_needed):
    name = get_name(ctx, param, is_needed)
    path = get_path(ctx, param, is_needed)
    return name, path


@click.command()
@click.option('--list', '-l', 'show', is_flag=True, help='List of persons in db')
@click.option('--delete', '-d', is_flag=True, callback=get_name, help='Delete person from db,'
                                                                      ' set name=\'all\' to wipe all data')
@click.option('--add-group', '-ag', is_flag=True, callback=get_path, help='Add group of persons to db')
@click.option('--add-person', '-ap', is_flag=True, callback=get_all, help='Add single person to db')
@click.option('--name', is_eager=True, help='Name of person to add/remove')
@click.option('--path', is_eager=True, help='Path to image data')
def main(show, delete, add_group, add_person, name, path):
    if show:
        show_persons()
    elif add_person != (None, None):
        INSERT_MANY = False

        insert_one_person(*add_person)
    elif add_group is not None:
        insert_many_persons(add_group)
    elif delete is not None:
        if delete == 'all':
            if click.confirm('Do you want to erase all data?'):
                delete_person()
        else:
            delete_person(delete)
    else:
        print('No flags provided')


if __name__ == '__main__':
    INSERT_MANY = False
    main()
