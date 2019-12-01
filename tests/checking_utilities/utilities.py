def is_face_inside(face_location, correct_location):
    x0_, w0_, y0_, h0_ = correct_location
    top, right, bottom, left = face_location
    return x0_ <= left and y0_ <= top and x0_ + w0_ >= right and y0_ + h0_ >= bottom