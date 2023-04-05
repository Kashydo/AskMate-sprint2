ID = 0

import csv


def generate_id(file):
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=",")
        last_id = list(reader)[-1][ID]
        return int(last_id) + 1
