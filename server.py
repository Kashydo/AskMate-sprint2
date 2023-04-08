from flask import Flask, render_template, request, redirect, url_for
import util
import datetime
import data_hendler
import csv
from config import *
from errors import *
from messages import *

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
        imagename = ""
        if len(title) == 0: errors_msg.append(errors["empty_title"])
        if len(message) == 0: errors_msg.append(errors["empty_message"])
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                if not util.is_allowed_file_extension(image.filename): errors_msg.append(errors["wrong_file_extension"])
                else:
                    imagename = IMAGES_FOLDER + str(question_id) + "." + util.get_file_extension(image.filename)
                    image.save(imagename)
        question = [question_id, submision_time, views, vote, title, message, imagename]
        if len(errors_msg) == 0:
            messages_msg = messages["added_question"]
            data_hendler.addtofile(question, QUESTIONS_FILE)
            return redirect(url_for("question_detail", question_id=question_id, messages_msg = messages_msg))
    return render_template("add_question.html", form = request.form, errors_msg = errors_msg)


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def answer(question_id):
    errors_msg = []
    if request.method == "POST":
        id = util.generate_id(ANSWER_FILE)
        submission_time = round(datetime.datetime.now().timestamp())
        vote_number = 0
        message = str(request.form.get("message"))
        image = request.form.get("image")
        answer = [id, submission_time, vote_number, question_id, message, image]
        if len(message) == 0: errors_msg.append(errors["empty_message"])
        if len(errors_msg) == 0:
            messages_msg = messages["added_answer"]
            data_hendler.addtofile(answer, ANSWER_FILE)
            return redirect(url_for("question_detail", question_id=question_id, messages_msg = messages_msg))
    return render_template("add_answer.html", question_id=question_id, form = request.form, errors_msg = errors_msg)


if __name__ == "__main__":
    app.run()
