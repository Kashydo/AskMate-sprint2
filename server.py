from flask import Flask, render_template, request, redirect, url_for
import util
import time
import data_hendler

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
def hello():
    return "Hello World!"


@app.route("/question")
def show_question():
    return "This is question"


@app.route("/add-question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        id = util.generate_id(QUESTIONS_FILE)
        submision_time = time.time_ns()
        views = 0
        vote = 0
        title = request.form.get("title")
        message = str(request.form.get("message"))
        image = request.form.get("image")
        question = [id, submision_time, views, vote, title, message, image]
        data_hendler.addtofile(question, QUESTIONS_FILE)
        return redirect("/")
    return render_template("add_question.html")


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def answer(question_id):
    if request.method == "POST":
        id = util.generate_id(ANSWER_FILE)
        submission_time = time.time_ns()
        vote_number = 0
        message = str(request.form.get("message"))
        image = request.form.get("image")
        answer = [id, submission_time, vote_number, question_id, message, image]
        data_hendler.addtofile(answer, ANSWER_FILE)
        return redirect("/")
    return render_template("add_answer.html", question_id=question_id)


if __name__ == "__main__":
    app.run()
