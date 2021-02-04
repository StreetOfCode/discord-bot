CREATE TABLE survey(
    survey_id SERIAL PRIMARY KEY,
    survey_info TEXT NOT NULL,
    survey_intro_message TEXT NOT NULL,
    receive_role_after_finish TEXT DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE user_survey_status_type AS ENUM('IN_PROGRESS', 'FINISHED', 'FINISHED_CHANNEL_DELETED');

CREATE TABLE user_survey_progress(
    user_survey_progress_id SERIAL PRIMARY KEY,
    survey_id INT REFERENCES survey(survey_id) ON DELETE CASCADE NOT NULL,
    user_id BIGINT NOT NULL,
    channel_id BIGINT NOT NULL,
    status user_survey_status_type NOT NULL DEFAULT 'IN_PROGRESS',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);


CREATE TABLE survey_question(
    survey_question_id SERIAL PRIMARY KEY,
    survey_id INT REFERENCES survey(survey_id) ON DELETE CASCADE NOT NULL,
    _order INT NOT NULL,
    text TEXT NOT NULL,
    is_multiple_choice BOOLEAN NOT NULL
);

CREATE TABLE survey_answer(
  survey_answer_id SERIAL PRIMARY KEY,
  survey_question_id INT REFERENCES survey_question(survey_question_id) ON DELETE CASCADE NOT NULL,
  _order INT NOT NULL,
  text TEXT NOT NULL,
  emoji TEXT NOT NULL,
  alias TEXT DEFAULT NULL UNIQUE
);

CREATE TABLE sent_survey_question(
  sent_survey_question_id SERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  survey_question_id INT REFERENCES survey_question(survey_question_id) ON DELETE CASCADE NOT NULL,
  message_id BIGINT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE user_survey_answer(
  user_id BIGINT NOT NULL,
  survey_question_id INT REFERENCES survey_question(survey_question_id) ON DELETE CASCADE NOT NULL,
  survey_answer_id INT REFERENCES survey_answer(survey_answer_id) ON DELETE CASCADE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-------------------  WELCOME SURVEY  ---------------------

INSERT INTO survey(survey_info, survey_intro_message)
VALUES ('welcome survey', E'Ahoj, ja som Street of Code bot a chcem sa ťa opýtať pár otázok. Tvoje odpovede vidia iba admini.\n\nCieľom tohto dotazníka je zistiť pár základných informácií.\n\nSmajlíky ber s prosím s rezervou. Ďakujem :)');


INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(1, 1, 'Pohlavie', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(1, 1, 'Muž', '🦸‍♂️');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(1, 2, 'Žena', '🦸‍♀️');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(1, 3, 'Iné', '⚪');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(1, 4, 'Nechcem odpovedať', '❔');


INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(1, 2, 'Vek', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(2, 1, '0 - 17', '👶');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(2, 2, '18 - 22', '🧑‍🦱');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(2, 3, '23 - 27', '👱‍♀️');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(2, 4, '28 - 34', '🧔');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(2, 5, '35 a viac', '👨‍🦲');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(2, 6, 'Nechcem odpovedať', '❔');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(1, 3, 'Ako si na tom s programovaním?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(3, 1, 'Chcem sa naučiť programovať', '🤓');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(3, 2, 'Už viem niečo naprogramovať', '🥳');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(3, 3, 'Pracujem ako programátor', '😎');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(1, 4, 'Počúvaš naše podcasty?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(4, 1, 'Počul/a som jednu alebo dve epizódy', '🙂');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji, alias)
VALUES(4, 2, 'Viac ako 2 epizódy', '😋', 'podcast-fan');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(4, 3, 'Zatiaľ nie', '🥲');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(1, 5, 'Aký obsah by si od nás privítal/a najčastejšie?', TRUE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(5, 1, 'Podcasty', '🎙️');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(5, 2, 'Videá o programovaní', '📷');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(5, 3, 'Články o programovaní', '📝');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(5, 4, 'Kurzy o programovaní', '🎥');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(1, 6, 'Môžeme ti v budúcnosti posielať takéto krátke dotazníky?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji, alias)
VALUES(6, 1, 'Áno', '👍', 'survey-fan');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(6, 2, 'Nie, ďakujem', '👎');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(1, 7, 'Odpovedal/a si na všetky otázky? Ked pridáš 👍, tak tieto odpovede už nebudeš môcť meniť a dokončíš dotazník.', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(7, 1, 'Áno', '👍');
