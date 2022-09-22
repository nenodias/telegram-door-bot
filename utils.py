from datetime import datetime


def get_now():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")