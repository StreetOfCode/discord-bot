import psycopg2
from config import DB_CONNECTION_STRING

db = psycopg2.connect(DB_CONNECTION_STRING)


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


def get_next_survey_question(user_id, survey_id):
    cursor = db.cursor()
    cursor.execute(
        f"""
            SELECT * FROM survey_question 
            WHERE survey_id = {survey_id} 
                AND survey_question_id 
                    NOT IN (
                        SELECT survey_question_id FROM user_survey_answer WHERE user_id = {user_id}
                    )
            ORDER BY survey_question_id
            LIMIT 1
        """
    )

    question = cursor.fetchone()
    if question is None:
        return None, None

    answers = get_survey_question_answers(question[0])
    if answers is None or len(answers) == 0:
        return None, None

    return question, answers


def get_survey_question_answers(question_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT * FROM survey_answer WHERE survey_question_id={question_id}"
    )
    return cursor.fetchall()


def get_emoji_from_survey_answer(survey_answer_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT emoji FROM survey_answer WHERE survey_answer_id={survey_answer_id}"
    )
    return cursor.fetchone()[0]


def add_sent_survey_question(user_id, survey_question_id, message_id):
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO sent_survey_question(user_id, survey_question_id, message_id) VALUES({user_id}, {survey_question_id}, {message_id})"
    )
    db.commit()


def create_user_survey_progress(survey_id, user_id, channel_id):
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO user_survey_progress(survey_id, user_id, channel_id) VALUES({survey_id}, {user_id}, {channel_id})"
    )
    db.commit()


def finish_user_survey_progress(survey_id, user_id):
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE user_survey_progress SET status='FINISHED' WHERE survey_id={survey_id} AND user_id={user_id}"
    )
    db.commit()


def add_answer(user_id, survey_question_id, survey_answer_id):
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO user_survey_answer(user_id, survey_question_id, survey_answer_id) VALUES({user_id}, {survey_question_id}, {survey_answer_id})"
    )
    db.commit()


def get_survey_intro_message(survey_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_intro_message from survey WHERE survey_id={survey_id}"
    )
    return cursor.fetchone()[0]


def get_survey_receive_role_or_none(survey_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT receive_role_after_finish from survey WHERE survey_id={survey_id}"
    )
    receive_role = cursor.fetchone()
    if receive_role is None:
        return receive_role
    else:
        return receive_role[0]


def get_survey_question_id_or_none(message_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_question_id FROM sent_survey_question WHERE message_id={message_id}"
    )

    question_id = cursor.fetchone()
    if question_id is None:
        return question_id
    else:
        return question_id[0]


def get_survey_id_from_user_survey_progress_or_none(user_id, channel_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_id FROM user_survey_progress WHERE user_id={user_id} AND channel_id={channel_id}"
    )
    survey_id = cursor.fetchone()
    if survey_id is None:
        return survey_id
    else:
        return survey_id[0]


def get_answer_id(survey_question_id, emoji):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_answer_id FROM survey_answer WHERE survey_question_id={survey_question_id} AND emoji='{emoji}'"
    )

    return cursor.fetchone()[0]


def get_answer_of_answered_survey_question_or_none(survey_question_id, user_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_answer_id FROM user_survey_answer WHERE survey_question_id={survey_question_id} AND user_id={user_id}"
    )

    answer_id = cursor.fetchone()
    if answer_id is None:
        return answer_id
    else:
        return answer_id[0]


def remove_user_answer(user_id, survey_question_id, survey_answer_id):
    cursor = db.cursor()
    cursor.execute(
        f"DELETE FROM user_survey_answer WHERE user_id={user_id} AND survey_question_id={survey_question_id} AND survey_answer_id={survey_answer_id}"
    )
    db.commit()


def are_all_survey_questions_answered(user_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT COUNT(*) FROM survey_question WHERE survey_question_id not in (SELECT survey_question_id FROM user_survey_answer WHERE user_id={user_id})"
    )

    return cursor.fetchone()[0] == 0
