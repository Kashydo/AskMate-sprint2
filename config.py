QUESTION_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
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
ID = 0
SUBMISSION_TIME = 1
VIEW_QUESTION, VOTE_ANSWER = 2, 2
VOTE_QUESTION, QUESTION_ID = 3, 3
TITLE, ANSWER = 4, 4
QUESTION, IMAGE_ANSWER = 5, 5
IMAGE_QUESTION = 6

QUESTIONS_FILE = "sample_data\question.csv"
ANSWER_FILE = "sample_data\Answer.csv"

IMAGES_FOLDER = "static/images/"
ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "gif", "bmp")
