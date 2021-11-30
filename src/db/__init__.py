import psycopg2

import survey_status
from config import DB_CONNECTION_STRING
from db.columns import COLUMN_SURVEY_ANSWER_ID, COLUMN_SURVEY_ANSWER_TEXT

db = psycopg2.connect(DB_CONNECTION_STRING)


def is_multiple_choice_survey_question(question_id):
    question = _fetchone(
        f"SELECT is_multiple_choice FROM survey_question WHERE survey_question_id={question_id}"
    )
    return question[0] if question is not None else False


def is_open_ended_survey_question(question_id):
    question = _fetchone(
        f"SELECT is_open_ended FROM survey_question WHERE survey_question_id={question_id}"
    )
    return question[0] if question is not None else False


def get_survey_question_order_or_none(question_id):
    question = _fetchone(
        f"SELECT _order FROM survey_question WHERE survey_question_id = {question_id}"
    )
    return _get_first_or_none(question)


def get_show_stats_updated_at_with_url_or_none(stat_id):
    row = _fetchone(
        f"SELECT updated_at, url FROM show_stats_cache WHERE stat_id = {stat_id}"
    )
    if row is None:
        return None
    return row[0], row[1]


def add_show_stats_cache(stat_id, url):
    _execute(f"INSERT INTO show_stats_cache(stat_id, url) VALUES({stat_id}, '{url}')")


def get_next_survey_question(user_id, survey_id):
    query = f"""
        SELECT * FROM survey_question 
        WHERE survey_id = {survey_id} 
            AND survey_question_id 
                NOT IN (
                    SELECT survey_question_id FROM sent_survey_question WHERE user_id = {user_id}
                )
        ORDER BY survey_question_id
        LIMIT 1
    """

    question = _fetchone(query)
    if question is None:
        return None, None

    answers = get_survey_question_answers(question[0])
    if answers is None:
        return None, None

    return question, answers


def get_answer_alias_survey_answer_id(alias):
    survey_answer_id = _fetchone(
        f"SELECT survey_answer_id FROM survey_answer WHERE alias='{alias}'"
    )
    return _get_first_or_none(survey_answer_id)


def get_survey_channel_name_suffix(survey_id):
    channel_name_suffix = _fetchone(
        f"SELECT channel_name_suffix FROM survey WHERE survey_id={survey_id}"
    )
    return _get_first_or_none(channel_name_suffix)


def check_survey_exists(survey_id):
    survey = _fetchone(f"SELECT survey_id from survey WHERE survey_id={survey_id}")
    return _get_first_or_none(survey) is not None


# Users which have previously answered on survey with answer which have this alias
def find_all_answer_alias_responders(alias):
    if (survey_answer_id := get_answer_alias_survey_answer_id(alias)) is not None:
        query = f"SELECT user_id FROM user_survey_answer WHERE survey_answer_id={survey_answer_id}"
        return [res[0] for res in _fetchall(query)]


def get_survey_question_answers(question_id):
    return _fetchall(
        f"SELECT * FROM survey_answer WHERE survey_question_id={question_id} ORDER BY survey_answer_id ASC"
    )


def get_emoji_from_survey_answer(survey_answer_id):
    query = f"SELECT emoji FROM survey_answer WHERE survey_answer_id={survey_answer_id}"
    return _fetchone(query)[0]


def add_sent_survey_question(user_id, survey_question_id, message_id):
    _execute(
        f"INSERT INTO sent_survey_question(user_id, survey_question_id, message_id) VALUES({user_id}, {survey_question_id}, {message_id})"
    )


def get_all_user_ids_from_survey_progress(survey_id):
    query = f"SELECT user_id from user_survey_progress WHERE survey_id={survey_id}"
    return [res[0] for res in _fetchall(query)]


def get_user_survey_progress_status_or_none(survey_id, user_id):
    status = _fetchone(
        f"SELECT status from user_survey_progress WHERE survey_id={survey_id} AND user_id={user_id}"
    )
    return _get_first_or_none(status)


def clear_all_user_survey_progress(survey_id, user_id):
    query = (
        f"SELECT survey_question_id from survey_question WHERE survey_id={survey_id}"
    )
    survey_question_ids = [res[0] for res in _fetchall(query)]
    survey_question_ids_to_string = ",".join(map(str, survey_question_ids))

    with db, db.cursor() as delete_cursor:
        delete_cursor.execute(
            f"DELETE from sent_survey_question WHERE user_id={user_id} AND survey_question_id IN ({survey_question_ids_to_string})"
        )
        delete_cursor.execute(
            f"DELETE from user_survey_answer WHERE user_id={user_id} AND survey_question_id IN ({survey_question_ids_to_string})"
        )
        delete_cursor.execute(
            f"DELETE from user_survey_progress WHERE survey_id={survey_id} AND user_id={user_id}"
        )


def create_user_survey_progress(survey_id, user_id, channel_id):
    _execute(
        f"INSERT INTO user_survey_progress(survey_id, user_id, channel_id) VALUES({survey_id}, {user_id}, {channel_id})"
    )


def finish_user_survey_progress(survey_id, user_id):
    _execute(
        f"UPDATE user_survey_progress SET status='{survey_status.FINISHED}', finished_at=NOW() WHERE survey_id={survey_id} AND user_id={user_id}"
    )


def set_user_survey_progress_status(channel_id, status):
    _execute(
        f"UPDATE user_survey_progress SET status='{status}' WHERE channel_id={channel_id}"
    )


def add_answer(user_id, survey_question_id, survey_answer_id):
    _execute(
        f"INSERT INTO user_survey_answer(user_id, survey_question_id, survey_answer_id) VALUES({user_id}, {survey_question_id}, {survey_answer_id})"
    )


def add_open_ended_answer(user_id, survey_question_id, answer, message_id):
    with db, db.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO user_survey_answer(user_id, survey_question_id, text, message_id) VALUES({user_id}, {survey_question_id}, %s, {message_id})",
            (answer,),
        )


def get_survey_intro_message(survey_id):
    query = f"SELECT survey_intro_message from survey WHERE survey_id={survey_id}"
    return _fetchone(query)[0]


def get_survey_receive_role_or_none(survey_id):
    receive_role = _fetchone(
        f"SELECT receive_role_after_finish from survey WHERE survey_id={survey_id}"
    )
    return _get_first_or_none(receive_role)


def get_survey_question_id_or_none(message_id):
    question_id = _fetchone(
        f"SELECT survey_question_id FROM sent_survey_question WHERE message_id={message_id}"
    )
    return _get_first_or_none(question_id)


def get_open_ended_question_id_from_answer_or_none(message_id):
    question_id = _fetchone(
        f"SELECT survey_question_id FROM user_survey_answer WHERE message_id={message_id}"
    )
    return _get_first_or_none(question_id)


def get_current_survey_question_or_none(user_id, survey_id):
    query = f"""
        SELECT * FROM survey_question 
        WHERE survey_id = {survey_id} 
            AND survey_question_id 
                IN (
                    SELECT survey_question_id FROM sent_survey_question WHERE user_id = {user_id}
                )
        ORDER BY survey_question_id DESC
        LIMIT 1
    """
    return _fetchone(query)


def get_survey_id_from_user_survey_progress_or_none(user_id, channel_id):
    survey_id = _fetchone(
        f"SELECT survey_id FROM user_survey_progress WHERE user_id={user_id} AND channel_id={channel_id}"
    )
    return _get_first_or_none(survey_id)


def is_survey_progress_finished(survey_id, user_id):
    status = _fetchone(
        f"SELECT status FROM user_survey_progress WHERE survey_id={survey_id} AND user_id={user_id}"
    )
    return _get_first_or_none(status) == survey_status.FINISHED


def get_answer_id(survey_question_id, emoji):
    query = f"SELECT survey_answer_id FROM survey_answer WHERE survey_question_id={survey_question_id} AND emoji='{emoji}'"
    return _fetchone(query)[0]


def get_answer_of_answered_survey_question_or_none(survey_question_id, user_id):
    result = _fetchone(
        f"SELECT survey_answer_id, text FROM user_survey_answer WHERE survey_question_id={survey_question_id} AND user_id={user_id}"
    )

    if result is None:
        return None, None

    return result


def remove_user_answer(
    user_id, survey_question_id, survey_answer_id=None, survey_answer_text=None
):
    if survey_answer_id is not None:
        _execute(
            f"DELETE FROM user_survey_answer WHERE user_id={user_id} AND survey_question_id={survey_question_id} AND survey_answer_id={survey_answer_id}"
        )
    elif survey_answer_text is not None:
        _execute(
            f"DELETE FROM user_survey_answer WHERE user_id={user_id} AND survey_question_id={survey_question_id} AND text='{survey_answer_text}'"
        )
    else:
        raise ValueError("Both survey_answer_id and survey_answer_text are None")


def remove_single_show_stats_cache(stat_id):
    _execute(f"DELETE FROM show_stats_cache WHERE stat_id={stat_id}")


def remove_all_show_stats_cache():
    _execute(f"DELETE FROM show_stats_cache")


def are_all_survey_questions_answered(user_id, survey_id):
    query = f"SELECT COUNT(*) FROM survey_question WHERE survey_id={survey_id} AND survey_question_id not in (SELECT survey_question_id FROM user_survey_answer WHERE user_id={user_id})"
    return _fetchone(query)[0] == 0


def is_last_question(survey_id, question_id):
    query = f"SELECT survey_question_id FROM survey_question WHERE survey_id={survey_id} ORDER BY survey_question_id DESC LIMIT 1"
    last_question = _fetchone(query)

    return last_question[0] == question_id if last_question is not None else False


def get_unanswered_question_texts(survey_id, user_id):
    query = f"SELECT text FROM survey_question WHERE survey_id={survey_id} AND survey_question_id not in (SELECT survey_question_id FROM user_survey_answer WHERE survey_id={survey_id} AND user_id={user_id})"
    return [res[0] for res in _fetchall(query)]


def get_all_in_progress_users_with_channel_from_survey_progress_created_older_than(
    survey_id, minus_interval
):
    """
    Returns map of user -> channel where every user started but not finished survey which was created no longer than {minus_interval}
    """
    query = f"SELECT user_id, channel_id from user_survey_progress WHERE survey_id={survey_id} and status = '{survey_status.IN_PROGRESS}' and created_at < (NOW() - INTERVAL '{minus_interval}')"
    return {user_id: channel_id for user_id, channel_id in _fetchall(query)}


def get_completed_survey_channel_ids_older_than(minus_interval):
    query = f"SELECT channel_id FROM user_survey_progress u WHERE status='{survey_status.FINISHED}' AND finished_at < (NOW() - INTERVAL '{minus_interval}')"
    return [res[0] for res in _fetchall(query)]


def get_in_progress_survey_channel_ids_older_than(minus_interval):
    query = f"SELECT channel_id FROM user_survey_progress u WHERE status='{survey_status.IN_PROGRESS}' AND created_at < (NOW() - INTERVAL '{minus_interval}')"
    return [res[0] for res in _fetchall(query)]


def get_answer_ids_with_text_from_question_id(question_id):
    """
    Returns list of tuples - tuple(survey_answer_id, survey_answer_text)
    """
    return [
        (res[COLUMN_SURVEY_ANSWER_ID], res[COLUMN_SURVEY_ANSWER_TEXT])
        for res in get_survey_question_answers(question_id)
    ]


def get_user_answers_count(question_id, survey_answer_ids):
    """
    Returns list of tuples - tuple(survey_answer_id, count)
    """
    survey_answer_ids = ",".join(map(str, survey_answer_ids))
    query = f"SELECT survey_answer_id, count(*) FROM user_survey_answer WHERE survey_question_id = {question_id} AND survey_answer_id IN ({survey_answer_ids}) GROUP BY survey_answer_id"
    return [(res[0], res[1]) for res in _fetchall(query)]


def _execute(query):
    with db, db.cursor() as cursor:
        cursor.execute(query)


def _fetchall(query):
    with db, db.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def _fetchone(query):
    with db, db.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()


def _get_first_or_none(row):
    return row[0] if row is not None else None
