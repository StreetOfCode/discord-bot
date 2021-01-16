import psycopg2

import survey_status
from config import DB_CONNECTION_STRING

db = psycopg2.connect(DB_CONNECTION_STRING)


def _get_first_or_none(row):
    return row[0] if row is not None else None


def is_multiple_choice_survey_question(question_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT is_multiple_choice FROM survey_question WHERE survey_question_id={question_id}"
    )

    question = cursor.fetchone()
    return question[0] if question is not None else False


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


def get_survey_question_order_or_none(question_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT _order FROM survey_question WHERE survey_question_id = {question_id}"
    )

    question = cursor.fetchone()

    return _get_first_or_none(question)


def get_next_survey_question(user_id, survey_id):
    cursor = db.cursor()
    cursor.execute(
        f"""
            SELECT * FROM survey_question 
            WHERE survey_id = {survey_id} 
                AND survey_question_id 
                    NOT IN (
                        SELECT survey_question_id FROM sent_survey_question WHERE user_id = {user_id}
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


def get_all_user_ids_from_survey_progress(survey_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT user_id from user_survey_progress WHERE survey_id={survey_id}"
    )
    return [res[0] for res in cursor.fetchall()]


def get_user_survey_progress_status_or_none(survey_id, user_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT status from user_survey_progress WHERE survey_id={survey_id} AND user_id={user_id}"
    )
    status = cursor.fetchone()

    return _get_first_or_none(status)


def clear_all_user_survey_progress(survey_id, user_id):
    survey_question_cursor = db.cursor()
    survey_question_cursor.execute(
        f"SELECT survey_question_id from survey_question WHERE survey_id={survey_id}"
    )
    survey_question_ids = [res[0] for res in survey_question_cursor.fetchall()]
    survey_question_ids_to_string = ",".join(map(str, survey_question_ids))

    delete_cursor = db.cursor()
    delete_cursor.execute(
        f"DELETE from sent_survey_question WHERE user_id={user_id} AND survey_question_id IN ({survey_question_ids_to_string})"
    )
    delete_cursor.execute(
        f"DELETE from user_survey_answer WHERE user_id={user_id} AND survey_question_id IN ({survey_question_ids_to_string})"
    )
    delete_cursor.execute(
        f"DELETE from user_survey_progress WHERE survey_id={survey_id} AND user_id={user_id}"
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
        f"UPDATE user_survey_progress SET status='{survey_status.FINISHED}', finished_at=NOW() WHERE survey_id={survey_id} AND user_id={user_id}"
    )
    db.commit()


def set_user_survey_progress_status_to_channel_deleted(channel_id):
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE user_survey_progress SET status='{survey_status.FINISHED_CHANNEL_DELETED}' WHERE channel_id={channel_id}"
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

    return _get_first_or_none(receive_role)


def get_survey_question_id_or_none(message_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_question_id FROM sent_survey_question WHERE message_id={message_id}"
    )

    question_id = cursor.fetchone()

    return _get_first_or_none(question_id)


def get_survey_id_from_user_survey_progress_or_none(user_id, channel_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_id FROM user_survey_progress WHERE user_id={user_id} AND channel_id={channel_id}"
    )
    survey_id = cursor.fetchone()

    return _get_first_or_none(survey_id)


def is_survey_progress_finished(survey_id, user_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT status FROM user_survey_progress WHERE survey_id={survey_id} AND user_id={user_id}"
    )
    status = cursor.fetchone()

    return _get_first_or_none(status) == survey_status.FINISHED


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

    return _get_first_or_none(answer_id)


def remove_user_answer(user_id, survey_question_id, survey_answer_id):
    cursor = db.cursor()
    cursor.execute(
        f"DELETE FROM user_survey_answer WHERE user_id={user_id} AND survey_question_id={survey_question_id} AND survey_answer_id={survey_answer_id}"
    )
    db.commit()


def are_all_survey_questions_answered(user_id, survey_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT COUNT(*) FROM survey_question WHERE survey_id={survey_id} AND survey_question_id not in (SELECT survey_question_id FROM user_survey_answer WHERE user_id={user_id})"
    )

    return cursor.fetchone()[0] == 0


def is_last_question(survey_id, question_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT survey_question_id FROM survey_question WHERE survey_id={survey_id} ORDER BY survey_question_id DESC LIMIT 1"
    )

    last_question = cursor.fetchone()

    return last_question[0] == question_id if last_question is not None else False


def get_unanswered_question_texts(survey_id, user_id):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT text FROM survey_question WHERE survey_id={survey_id} AND survey_question_id not in (SELECT survey_question_id FROM user_survey_answer WHERE survey_id={survey_id} AND user_id={user_id})"
    )

    return [res[0] for res in cursor.fetchall()]


def get_all_in_progress_users_with_channel_from_survey_progress_created_older_than(
    survey_id, minus_interval
):
    """
    Returns map of user -> channel where every user started but not finished survey which was created no longer than {minus_interval}
    """
    cursor = db.cursor()
    cursor.execute(
        f"SELECT user_id, channel_id from user_survey_progress WHERE survey_id={survey_id} and status = '{survey_status.IN_PROGRESS}' and created_at < (NOW() - INTERVAL '{minus_interval}')"
    )
    return {user_id: channel_id for user_id, channel_id in cursor.fetchall()}


def get_all_users_with_no_answer(survey_id, user_ids):
    """
    Gets user_ids of every user who is IN user_ids from param but has no answer to any survey_question based on survey_id
    """
    #  users who are IN {users_in} and NOT IN (users who have answered at least one survey question)
    cursor = db.cursor()
    cursor.execute(
        f"""
        SELECT DISTINCT(user_id) FROM sent_survey_question WHERE user_id IN ({",".join(map(str, user_ids))}) AND user_id NOT IN (
            SELECT DISTINCT(user_id) FROM user_survey_answer WHERE survey_question_id IN (
                SELECT survey_question_id FROM survey_question WHERE survey_id={survey_id}
            )
        )
        """
    )
    return [res[0] for res in cursor.fetchall()]


def get_completed_survey_channel_ids_older_than(minus_interval):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT channel_id FROM user_survey_progress u WHERE status='{survey_status.FINISHED}' AND finished_at < (NOW() - INTERVAL '{minus_interval}')"
    )

    return [res[0] for res in cursor.fetchall()]
