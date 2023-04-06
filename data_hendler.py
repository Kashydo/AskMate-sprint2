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


def addtofile(data, file):
    with open(file, "a", newline="") as f:
        write = csv.writer(f)
        write.writerow(data)
