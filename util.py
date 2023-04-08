import datetime
import csv
import os.path
from config import *


def generate_id(file):
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=",")
        last_id = list(reader)[-1][ID]
        return int(last_id) + 1


ct = datetime.datetime.now()
ts = round(ct.timestamp())
print("timestamp:-", ts)


def is_allowed_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()