def error_flashing(error, error_type):
    if error == False:
        error_type = "None"
        return error, error_type
    else:
        error = True
        error_type = error_type
        return error, error_type