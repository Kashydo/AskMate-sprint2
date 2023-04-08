from flask import Flask, render_template, request, redirect, url_for
import util
import datetime
import data_hendler
import csv

QUESTION_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number" "title",
    "message",
    "image",
]

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
def question_detail(question_id):
    with open(QUESTIONS_FILE, "r", newline="") as csvfile:
        questions = list(csv.DictReader(csvfile))
    question = next((q for q in questions if q["id"] == question_id), None)
    return render_template("question_detail.html", question=question)


@app.route("/add-question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        question_id = util.generate_id(QUESTIONS_FILE)
        submision_time = round(datetime.datetime.now().timestamp())
        views = 0
        vote = 0
        title = request.form.get("title")
        message = str(request.form.get("message"))
        image = request.form.get("image")
        question = [question_id, submision_time, views, vote, title, message, image]
        data_hendler.addtofile(question, QUESTIONS_FILE)
        return redirect(url_for("question_detail", question_id=question_id))
    return render_template("add_question.html")


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def answer(question_id):
    if request.method == "POST":
        id = util.generate_id(ANSWER_FILE)
        submission_time = round(time.time())
        vote_number = 0
        message = str(request.form.get("message"))
        image = request.form.get("image")
        answer = [id, submission_time, vote_number, question_id, message, image]
        data_hendler.addtofile(answer, ANSWER_FILE)
        return redirect("/")
    return render_template("add_answer.html", question_id=question_id)


if __name__ == "__main__":
    app.run()
