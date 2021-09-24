from db.columns import (
    COLUMN_SURVEY_QUESTION_IS_MULTIPLE_CHOICE,
    COLUMN_SURVEY_QUESTION_IS_OPEN_ENDED,
)

MULTIPLE_CHOICE_EMBED_DESCRIPTION = " Môžeš zvoliť viacero odpovedí!"
OPEN_ENDED_QUESTION_EMBED_DESCRIPTION = (
    "Otázka má otvorenú (textovú) odpoveď! Odpovieš odoslaním správy do tohto kanála."
)


def is_question_multiple_choice(question):
    return question[COLUMN_SURVEY_QUESTION_IS_MULTIPLE_CHOICE]


def is_question_open_ended(question):
    return question[COLUMN_SURVEY_QUESTION_IS_OPEN_ENDED]


def get_question_description(question):
    if is_question_multiple_choice(question):
        return MULTIPLE_CHOICE_EMBED_DESCRIPTION
    elif is_question_open_ended(question):
        return OPEN_ENDED_QUESTION_EMBED_DESCRIPTION
    else:
        return ""
