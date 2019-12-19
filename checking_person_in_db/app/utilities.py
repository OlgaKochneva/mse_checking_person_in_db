types = {
    'err': '[ERROR] \033[91m {} \033[0m',
    'progress': '[PROGRESS] \033[92m {} \033[0m'
}


def msg(msg_type, text, log):
    log(types[msg_type].format(text))


# prototype of a function for proper detection of faces on frame
# found_face_names is a future attribute of FaceComparer class
# function will be moved there after task #19 completion
def handle_faces_presence(prev_face_names, detected_faces):
    prev_faces_set = set(prev_face_names)
    cur_faces_set = set(detected_faces)
    # faces that have been detected on prev frame but are not on current
    lost_faces = list(prev_faces_set - cur_faces_set)
    # faces that are detected on cur frame but haven't been detected on prev
    new_faces = list(cur_faces_set - prev_faces_set)
    return new_faces, lost_faces


# converts milliseconds to human readable format
def format_time(ms):
    min = round(ms / 1000) // 60
    sec = ms // 1000 % 60
    msec = ms % 1000
    return f'{min:02d}:{sec:02.0f}.{msec:03.0f}'


# spinner for video capture from cam
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor
