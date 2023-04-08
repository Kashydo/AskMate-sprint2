ID = 0
import datetime
import csv


def generate_id(file):
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=",")
        last_id = list(reader)[-1][ID]
        return int(last_id) + 1


ct = datetime.datetime.now()
ts = round(ct.timestamp())
print("timestamp:-", ts)
