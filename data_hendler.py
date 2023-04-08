import csv
import os


DATA_FILE_PATH = (
    os.getenv("DATA_FILE_PATH") if "DATA_FILE_PATH" in os.environ else "data.csv"
)
QUESTION_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number" "title",
    "message",
    "image",
]

ANSWER_HEADER = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image",
]


def addtofile(data, file):
    with open(file, "a", newline="") as f:
        write = csv.writer(f)
        write.writerow(data)


def readfile(file):
    with open(file, "r") as f:
        return list(csv.reader(f, delimiter=","))


def read_specific_data(file, serched_data, data):
    with open(file, "r") as f:
        return_data = []
        full_data = list(csv.DictReader(f))
        for e in full_data:
            if str(data) == e[serched_data]:
                return_data.append(e)
        if return_data == []:
            return_data = None
        return return_data
