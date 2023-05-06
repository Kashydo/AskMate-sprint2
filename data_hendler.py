import csv
import os
import datetime
from io import BytesIO

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import util
import database_common
from config import *
from errors import *
from messages import *


@database_common.connection_handler
def generate_id(cursor, table_name):
    query = f"""

        SELECT id
        FROM {table_name}
        ORDER BY submission_time DESC 
        LIMIT 1"""
    cursor.execute(query)
    result = cursor.fetchone()
    return result['id'] + 1 if result else 1

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


def find_data_in_list(data, list, key):
    return_list = []
    for e in list:
        if str(data) == e[key]:
            return_list.append(e)
    return return_list


def remove_data_from_list(list, data, key):
    return_list = []
    for e in list:
        if str(data) != e[key]:
            return_list.append(e)
    return return_list


@database_common.connection_handler
def add_vote(cursor, id, database):
    query = f"""
        UPDATE {database}
        SET vote_number = vote_number + 1
        WHERE id = {id}
        """
    cursor.execute(query)


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
def get_5_latest_questions(cursor):
    query = f"""
    SELECT *
    FROM questions
    ORDER BY submission_time desc
    LIMIT 5
    """
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
def read_answer(cursor, id):
    query = f"""
        SELECT *
        FROM answers
        WHERE id = {id}"""
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def read_comments(cursor,question_id):
    query = f"""
        SELECT id,  message, submission_time
        FROM comment 
        WHERE question_id = {question_id}"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def read_comments_to_answer(cursor,question_id, answer_id):
    query = f"""
        SELECT id,  message, submission_time
        FROM comments_to_answer 
        WHERE question_id = {question_id} AND answer_id={answer_id}"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def read_comment(cursor, id):
    query = f"""
        SELECT *
        FROM comment
        WHERE id = {id}"""
    cursor.execute(query)
    return cursor.fetchone()

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
def delete_question(cursor, question_id, user_id):
    errors_msg = []
    query = f"""
        SELECT image, user_id
        FROM questions
        WHERE id = {question_id}"""
    cursor.execute(query)
    question = cursor.fetchone()

    if user_id == question["user_id"]:
        query = f"""
            SELECT image
            FROM answers
            WHERE question_id = {question_id}"""
        cursor.execute(query)
        answers = cursor.fetchall()
        for answer in answers:
            if answer["image"] != "" and answer["image"] != None:
                os.remove(answer["image"])

        query = f"""
            DELETE FROM answers
            WHERE question_id = {question_id}"""
        cursor.execute(query)

        query = f"""
            DELETE FROM question_tag
            WHERE question_id = {question_id}
        """
        cursor.execute(query)

        query = f"""
            DELETE FROM questions
            WHERE id = {question_id}"""
        cursor.execute(query)

        if question["image"] != "" and question["image"] != None:
            os.remove(question["image"])
    else:
        errors_msg.append(errors["cant_delete"])

    return errors_msg


@database_common.connection_handler
def edit_question(cursor, question_id, title, message, image):
    query = """
    UPDATE questions
    SET title = %s,
    message = %s,
    image = %s
    WHERE question_id = %s
    """
    cursor.execute(query, (title, message, image, question_id))

@database_common.connection_handler
def edit_answer(cursor, answer_id, message, image):
    submission_time = round(datetime.datetime.now().timestamp())
    query = """
    UPDATE answers
    SET message = %s,
    image = %s,
    submission_time=%s
    WHERE id = %s
    """
    if image:
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        cursor.execute(query, (message, image_bytes.getvalue(), submission_time, answer_id))
    else:
        cursor.execute(query, (message, None, submission_time, answer_id))

@database_common.connection_handler
def edit_comment(cursor, answer_id, message):
    submision_time = round(datetime.datetime.now().timestamp())
    query = """
    UPDATE comment
    SET message = %s,
    submission_time=to_timestamp(%s)
    WHERE id = %s
    """
    cursor.execute(query, (message, submision_time, answer_id))

@database_common.connection_handler
def delete_answer(cursor, answer_id, user_id):
    errors_msg = []
    query = f"""
        SELECT image, user_id
        FROM answers
        WHERE id = {answer_id}"""
    cursor.execute(query)
    answer = cursor.fetchone()

    if user_id == answer["user_id"]:
        query = f"""
            DELETE FROM answers
            WHERE id = {answer_id}"""
        cursor.execute(query)

        if answer["image"] != "" and answer["image"] != None:
            os.remove(answer["image"])
    else:
        errors_msg.append(errors["cant_delete"])

    return errors_msg


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


@database_common.connection_handler
def find_answer(cursor, phrase):
    query = f"""
    SELECT *
    FROM answers
    WHERE message ILIKE '%{phrase}%'
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def find_question_and_answers(cursor, phrase):
    query = f"""
    SELECT t2.question_id, t1.title, t2.id, t2.message
    FROM questions t1
    RIGHT OUTER JOIN answers t2
    ON t1.id = t2.question_id
    WHERE  t2.message ILIKE '%{phrase}%'
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_tags(cursor):
    query = f"""
    SELECT DISTINCT name
    FROM tag
    ORDER BY name ASC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_by_name(cursor, tag_name):
    query = f"""
    SELECT *
    FROM tag
    WHERE  name = '{tag_name}'
    """
    cursor.execute(query)
    tag = cursor.fetchone()
    if tag:
        return tag
    else:
        return None


@database_common.connection_handler
def add_new_tag(cursor, tag_name):
    query = f"""
    INSERT INTO tag(name)
    VALUES ('{tag_name}')
    """
    cursor.execute(query)


@database_common.connection_handler
def add_tag_to_question(cursor, question_id, request):
    errors_msg = []
    tag_name = request.form.get("tag_name").lower()
    existing_tag = request.form.get("existing_tag")
    if existing_tag:
        tag = get_tag_by_name(existing_tag)
    else:
        if len(tag_name) == 0:
            errors_msg.append(errors["empty_tag"])
        else:
            tag = get_tag_by_name(tag_name)
            if not tag:
                tag = add_new_tag(tag_name)
                tag = get_tag_by_name(tag_name)
    tag_id = tag["id"]
    query = """
        SELECT EXISTS(
            SELECT 1 FROM question_tag
            WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
        );
    """
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})
    row = cursor.fetchone()
    if row is None:
        errors_msg.append("tag_exist")
    if len(errors_msg) == 0:
        query = f"""
        INSERT INTO question_tag(
        question_id, tag_id)
        VALUES ({question_id}, {tag["id"]});
        """
        cursor.execute(query)
        question_tag = cursor.lastrowid
    return errors_msg, question_tag


@database_common.connection_handler
def get_tags_for_question(cursor, question_id):
    query = f"""
    SELECT *
    FROM tag
    RIGHT OUTER JOIN question_tag
    ON tag.id = question_tag.tag_id
    WHERE question_id ={question_id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag(cursor, question_id, tag_id, user_id):
    errors_msg = []
    query = f"""
        SELECT user_id
        FROM questions
        WHERE id = {question_id}"""
    cursor.execute(query)
    questions = cursor.fetchone()
    if user_id == questions["user_id"]:
        query = f"""
            DELETE FROM question_tag
            WHERE question_id = {question_id} AND tag_id = {tag_id}"""
        cursor.execute(query)
    else:
        errors_msg.append(errors["cant_delete"])
    return errors_msg


@database_common.connection_handler
def add_comment(cursor, request, user_id, question_id):
    errors_msg = []
    comment_id = generate_id('comment')
    submission_time = round(datetime.datetime.now().timestamp())
    message = request.form.get("message")
    edited_count=0
    if len(message) == 0:
        errors_msg.append(errors["empty_message"])

    if len(errors_msg) == 0:
        query = f"""
            INSERT INTO comment(id,question_id, message, submission_time, edited_count, user_id)
            VALUES ({comment_id},{question_id},'{message}', to_timestamp({submission_time}) , '{edited_count}', '{user_id}')
            RETURNING id"""
        cursor.execute(query)

    return errors_msg, question_id

@database_common.connection_handler
def add_comment_to_answer(cursor, request, user_id, question_id, answer_id):
    errors_msg = []
    comment_id = generate_id('comment')
    submission_time = round(datetime.datetime.now().timestamp())
    message = request.form.get("message")
    edited_count=0
    if len(message) == 0:
        errors_msg.append(errors["empty_message"])

    if len(errors_msg) == 0:
        query = f"""
            INSERT INTO comments_to_answer(id,question_id,answer_id, message, submission_time, edited_count, user_id)
            VALUES ({comment_id},{question_id},{answer_id}, '{message}', to_timestamp({submission_time}) , '{edited_count}', '{user_id}')
            RETURNING id"""
        cursor.execute(query)

    return errors_msg, question_id,answer_id

@database_common.connection_handler
def delete_comment(cursor, comment_id, user_id):
    errors_msg = []
    query = f"""
        SELECT user_id
        FROM comment
        WHERE id = {comment_id}"""
    cursor.execute(query)
    comment = cursor.fetchone()
    if user_id == comment['user_id']:
        query = f"""
            DELETE FROM comment
            WHERE id = {comment_id}"""
        cursor.execute(query)

    return errors_msg
