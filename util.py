import datetime
import csv
import os.path
import random
import string
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

def generate_user_id(number_of_small_letters=4,
                number_of_capital_letters=2,
                number_of_digits=2,
                number_of_special_chars=2,
                allowed_special_chars=r"_+-!"):

    length = number_of_small_letters + number_of_capital_letters + number_of_digits + number_of_special_chars
    id = list(range(length))
    random_positions = []

    while len(random_positions) < length:
        random_number = random.randint(0,length-1)
        if random_number not in random_positions: random_positions.append(random_number)

    for i in range(number_of_small_letters):
        id[random_positions[0]] = random.choice(string.ascii_lowercase)
        del random_positions[0]
    for i in range(number_of_capital_letters):
        id[random_positions[0]] = random.choice(string.ascii_uppercase)
        del random_positions[0]
    for i in range(number_of_digits):
        id[random_positions[0]] = random.choice(string.digits)
        del random_positions[0]
    for i in range(number_of_special_chars):
        id[random_positions[0]] = random.choice(allowed_special_chars)
        del random_positions[0]

    return "".join(id)

def get_user_id(request):
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = generate_user_id()
    return user_id