from flask import Flask, render_template, request, redirect
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
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add-question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        id = util.generate_id(QUESTIONS_FILE)
        submision_time = time.time_ns()
        views = 0
        vote = 0
        title = request.form.get("title")
        message = request.form.get("message")
        image = request.form.get("image")
        question = [id, submision_time, views, vote, title, message, image]
        data_hendler.addtofile(question, QUESTIONS_FILE)
        return redirect("/")
    return render_template("add_question.html")


if __name__ == "__main__":
    app.run()
