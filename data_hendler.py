import csv
import os

QUESTIONS_FILE = "sample_data\question.csv"

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


def addquestion(question):
    with open(QUESTIONS_FILE, "a") as f:
        f.write(question)
