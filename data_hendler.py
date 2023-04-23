import csv
import os
import datetime

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import util
import database_common
from config import *
from errors import *
from messages import *

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


@database_common.connection_handler
def addquestion(cursor, new_question: dict):
    query = f"""
    INSERT INTO question(
	submission_time, view_number, vote_number, title, message, image,user_id)
	VALUES ('{new_question['submission_time']}','{new_question['view_number']}','{new_question['vote_number']}','{new_question['title']}','{new_question['message']}','{new_question['image']}','{new_question['user_id']}')
    """
    cursor.execute(query)


@database_common.connection_handler
def addanswer(cursor, new_answer: dict):
    query = f"""
    INSERT INTO answer(
	submission_time, vote_number,question_id, message, image,user_id)
	VALUES ('{new_answer['submission_time']}','{new_answer['vote_number']}','{new_answer['question_id']}','{new_answer['message']}','{new_answer['image']}','{new_answer['user_id']}')
    """
    cursor.execute(query)


@database_common.connection_handler
def readfile(file):
    with open(file, "r") as f:
        return list(csv.DictReader(f))


def find_data_in_list(data, list, key):
    return_list = []
    for e in list:
        if str(data) == e[key]:
            return_list.append(e)
    return return_list


def read_specific_data(file, key, data):
    full_data = readfile(file)
    return_data = find_data_in_list(data, full_data, key)
    if return_data == []:
        return_data = None
    return return_data


def write_new_file(file, headers, list):
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for dictionary in list:
            writer.writerow(dictionary.values())


def remove_data_from_list(list, data, key):
    return_list = []
    for e in list:
        if str(data) != e[key]:
            return_list.append(e)
    return return_list


def delete_data(file, data_to_delete, key, headers):
    old_file = readfile(file)
    new_file = remove_data_from_list(old_file, data_to_delete, key)
    write_new_file(file, headers, new_file)


def add_vote_in_list(list, data, key):
    return_list = []
    for e in list:
        if str(data) == e[key]:
            e["vote_number"] = int(e["vote_number"]) + 1
            e["vote_number"] = str(e["vote_number"])
        return_list.append(e)
    return return_list


def add_vote(file, data_to_delete, key, headers):
    old_file = readfile(file)
    new_file = add_vote_in_list(old_file, data_to_delete, key)
    write_new_file(file, headers, new_file)


def get_order_string(order_by, order_direction):
    order_string = ""
    match order_by:
        case "title":
            order_string = " ORDER BY title"
        case "submission_time":
            order_string = " ORDER BY submission_time"
        case "vote_number":
            order_string = " ORDER BY vote_number"

    if order_string != "" and order_direction == "desc":
        order_string += " DESC"
    return order_string


@database_common.connection_handler
def read_questions(cursor, order_by=None, order_direction=None):
    order_string = get_order_string(order_by, order_direction)
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image, user_id
        FROM questions
        {order_string}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def read_question(cursor, id):
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image, user_id
        FROM questions
        WHERE id = {id}"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def read_answers(cursor, question_id, order_by=None, order_direction=None):
    order_string = get_order_string(order_by, order_direction)
    query = f"""
        SELECT id, submission_time, vote_number, message, image, user_id
        FROM answers
        WHERE question_id = {question_id}
        {order_string}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor, request, user_id):
    errors_msg = []
    question_id = 0
    submision_time = datetime.datetime.now().timestamp()
    view_number = 0
    vote_number = 0
    title = request.form.get("title")
    message = request.form.get("message")
    imagename = ""
    if len(title) == 0:
        errors_msg.append(errors["empty_title"])
    if len(message) == 0:
        errors_msg.append(errors["empty_message"])
    if "image" in request.files:
        image = request.files["image"]
        imagename = image.filename
        if imagename != "":
            if not util.is_allowed_file_extension(imagename):
                errors_msg.append(errors["wrong_file_extension"])

    if len(errors_msg) == 0:
        query = f"""
            INSERT INTO questions(
            submission_time, view_number, vote_number, title, message, image, user_id)
            VALUES ({submision_time}, {view_number}, {vote_number}, '{title}', '{message}', '', '{user_id}')
            RETURNING id"""
        cursor.execute(query)
        question_id = cursor.fetchone()["id"]

        if imagename != "":
            imagename = (
                IMAGES_FOLDER
                + str(question_id)
                + "."
                + util.get_file_extension(imagename)
            )
            image.save(imagename)
            query = f"""
                UPDATE questions
                SET image='{imagename}'
                WHERE id={question_id}"""
            cursor.execute(query)

    return errors_msg, question_id


@database_common.connection_handler
def add_answer(cursor, request, user_id, question_id):
    errors_msg = []
    answer_id = 0
    submision_time = round(datetime.datetime.now().timestamp())
    vote_number = 0
    message = request.form.get("message")
    imagename = ""
    if len(message) == 0:
        errors_msg.append(errors["empty_message"])
    if "image" in request.files:
        image = request.files["image"]
        imagename = image.filename
        if imagename != "":
            if not util.is_allowed_file_extension(imagename):
                errors_msg.append(errors["wrong_file_extension"])

    if len(errors_msg) == 0:
        query = f"""
            INSERT INTO answers(
            question_id, submission_time, vote_number, message, image, user_id)
            VALUES ({question_id}, {submision_time}, {vote_number}, '{message}', '', '{user_id}')
            RETURNING id"""
        cursor.execute(query)
        answer_id = cursor.fetchone()["id"]

        if imagename != "":
            imagename = (
                IMAGES_FOLDER
                + str(question_id)
                + "-"
                + str(answer_id)
                + "."
                + util.get_file_extension(imagename)
            )
            image.save(imagename)
            query = f"""
                UPDATE answers
                SET image='{imagename}'
                WHERE id={answer_id}"""
            cursor.execute(query)

    return errors_msg, question_id


@database_common.connection_handler
def add_answer(cursor, request, user_id, question_id):
    errors_msg = []
    answer_id = 0
    submision_time = round(datetime.datetime.now().timestamp())
    vote_number = 0
    message = request.form.get("message")
    imagename = ""
    if len(message) == 0:
        errors_msg.append(errors["empty_message"])
    if "image" in request.files:
        image = request.files["image"]
        imagename = image.filename
        if imagename != "":
            if not util.is_allowed_file_extension(imagename):
                errors_msg.append(errors["wrong_file_extension"])

    if len(errors_msg) == 0:
        query = f"""
            INSERT INTO answers(
            question_id, submission_time, vote_number, message, image, user_id)
            VALUES ({question_id}, {submision_time}, {vote_number}, '{message}', '', '{user_id}')
            RETURNING id"""
        cursor.execute(query)
        answer_id = cursor.fetchone()["id"]

        if imagename != "":
            imagename = (
                IMAGES_FOLDER
                + str(question_id)
                + "-"
                + str(answer_id)
                + "."
                + util.get_file_extension(imagename)
            )
            image.save(imagename)
            query = f"""
                UPDATE answers
                SET image='{imagename}'
                WHERE id={answer_id}"""
            cursor.execute(query)

    return errors_msg, question_id


@database_common.connection_handler
def find_question(cursor, phrase):
    query = f"""
    SELECT id, submission_time, view_number, vote_number, title, message, image, user_id
    FROM questions
    WHERE title ILIKE '%{phrase}%'
    OR
    message ILIKE '%{phrase}%'
    """
    cursor.execute(query)
    return cursor.fetchall()
