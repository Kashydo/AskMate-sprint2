from flask import Flask, render_template, request, redirect
import util
import time
import data_hendler

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add-question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        question = [
            util.generate_id,
            time.thread_time_ns(),
            0,
            0,
            request.form.get("title"),
            request.form.get("message"),
            request.form.get("image"),
        ]
        data_hendler.addquestion(question)
        return redirect("/")


if __name__ == "__main__":
    app.run()
