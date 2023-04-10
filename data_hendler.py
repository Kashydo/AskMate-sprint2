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
    "user_id",
]

ANSWER_HEADER = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image",
    "user_id",
]


def addtofile(data, file):
    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)


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


def delete_data(file, data_to_delete, data_category, headers):
    with open(file, "r") as f:
        old_file = list(csv.DictReader(f))
        new_file = []
        for e in old_file:
            if str(data_to_delete) != e[data_category]:
                new_file.append(e)
    f.close()
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for dictionary in new_file:
            writer.writerow(dictionary.values())
