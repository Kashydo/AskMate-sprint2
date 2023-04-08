from flask import Flask, render_template, request, redirect, url_for
import util
import datetime
import data_hendler
import csv
from errors import *
from messages import *

QUESTION_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
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
ID = 0
SUBMISSION_TIME = 1
VIEW_QUESTION, VOTE_ANSWER = 2, 2
VOTE_QUESTION, QUESTION_ID = 3, 3
TITLE, ANSWER = 4, 4
QUESTION, IMAGE_ANSWER = 5, 5
IMAGE_QUESTION = 6

QUESTIONS_FILE = "sample_data\question.csv"
ANSWER_FILE = "sample_data\Answer.csv"
app = Flask(__name__)


@app.route("/")
@app.route("/")
@app.route("/list")
def question_list():
    with open(QUESTIONS_FILE, "r", newline="") as csvfile:
        questions = list(csv.DictReader(csvfile))
    return render_template("question_list.html", user_questions=questions)


@app.route("/question/<question_id>")
@app.route("/question/<question_id>/<string:messages_msg>")
def question_detail(question_id, messages_msg = None):
    with open(QUESTIONS_FILE, "r", newline="") as csvfile:
        questions = list(csv.DictReader(csvfile))
    question = next((q for q in questions if q["id"] == question_id), None)
    answers_to_question = data_hendler.read_specific_data(
        ANSWER_FILE, "question_id", question_id
    )
    return render_template(
        "question_detail.html", question=question, answers=answers_to_question, messages_msg = messages_msg
    )


@app.route("/add-question", methods=["GET", "POST"])
def question():
    errors_msg = []
    if request.method == "POST":
        question_id = util.generate_id(QUESTIONS_FILE)
        submision_time = round(datetime.datetime.now().timestamp())
        views = 0
        vote = 0
        title = request.form.get("title")
        message = str(request.form.get("message"))
        image = request.form.get("image")
        question = [question_id, submision_time, views, vote, title, message, image]
        if len(title) == 0: errors_msg.append(errors["empty_title"])
        if len(message) == 0: errors_msg.append(errors["empty_message"])
        if len(errors_msg) == 0:
            messages_msg = messages["added_question"]
            data_hendler.addtofile(question, QUESTIONS_FILE)
            return redirect(url_for("question_detail", question_id=question_id, messages_msg = messages_msg))
    return render_template("add_question.html", form = request.form, errors_msg = errors_msg)


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def answer(question_id):
    if request.method == "POST":
        id = util.generate_id(ANSWER_FILE)
        submission_time = round(datetime.datetime.now().timestamp())
        vote_number = 0
        message = str(request.form.get("message"))
        image = request.form.get("image")
        answer = [id, submission_time, vote_number, question_id, message, image]
        data_hendler.addtofile(answer, ANSWER_FILE)
        return redirect(url_for("question_detail", question_id=question_id))
    return render_template("add_answer.html", question_id=question_id)


if __name__ == "__main__":
    app.run()
