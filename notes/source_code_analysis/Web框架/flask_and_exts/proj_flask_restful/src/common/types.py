

def password_type(password):
    if len(password) < 6:
        raise ValueError('The password is too short.')
    return password
