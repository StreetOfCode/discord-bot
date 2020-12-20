import psycopg2
from config import DB_CONNECTION_STRING

db = psycopg2.connect(DB_CONNECTION_STRING)


def add_test(value):
    cursor = db.cursor()
    cursor.execute("INSERT INTO TEST(test) VALUES('" + value + "')")
    db.commit()


def get_survey_questions():
    questions_cursor = db.cursor()
    questions_cursor.execute("SELECT * FROM survey_question")

    result = []
    question = questions_cursor.fetchone()
    while question is not None:
        answers_cursor = db.cursor()
        answers_cursor.execute(
            f"SELECT * FROM survey_answer WHERE survey_question_id={question[0]}"
        )
        answers = answers_cursor.fetchall()
        result.append((question, answers))

        question = questions_cursor.fetchone()

    return result


def add_sent_survey_question(user_id, survey_question_id, message_id):
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO sent_survey_question(user_id, survey_question_id, message_id) VALUES({user_id}, {survey_question_id}, {message_id})"
    )
    db.commit()


def add_answer(user_id, survey_question_id, survey_answer_id):
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO user_survey_answer(user_id, survey_question_id, survey_answer_id) VALUES({user_id}, {survey_question_id}, {survey_answer_id})"
    )
    db.commit()


def get_survey_question_id(message_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_question_id FROM sent_survey_question WHERE message_id={message_id}"
    )

    return cursor.fetchone()[0]


def get_answer_id(survey_question_id, emoji):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_answer_id FROM survey_answer WHERE survey_question_id={survey_question_id} AND emoji='{emoji}'"
    )

    return cursor.fetchone()[0]


def are_all_survey_questions_answered(user_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT COUNT(*) FROM survey_question WHERE survey_question_id not in (SELECT survey_question_id FROM user_survey_answer WHERE user_id={user_id})"
    )

    return cursor.fetchone()[0] == 0
