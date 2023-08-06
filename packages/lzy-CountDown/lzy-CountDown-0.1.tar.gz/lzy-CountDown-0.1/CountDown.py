import time
def CountDown(*args):
    return int(time.mktime(time.strptime(*args, "%Y-%m-%d %H:%M:%S")))-int(time.time())