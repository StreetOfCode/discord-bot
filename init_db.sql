DROP TABLE IF EXISTS test;
CREATE TABLE test(id SERIAL PRIMARY KEY, test TEXT);

------------------ TABLE DEFINITIONS ---------------

DROP TABLE IF EXISTS quiz CASCADE;
DROP TABLE IF EXISTS survey_question CASCADE;
DROP TABLE IF EXISTS survey_answer CASCADE;
DROP TABLE IF EXISTS sent_survey_question CASCADE;
DROP TABLE IF EXISTS user_survey_answer CASCADE;


CREATE TABLE quiz(
    quiz_id SERIAL PRIMARY KEY,
    quiz_info TEXT NOT NULL,
    quiz_intro_message TEXT NOT NULL,
    receive_role_after_finish TEXT DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE survey_question(
    survey_question_id SERIAL PRIMARY KEY,
    quiz_id INT REFERENCES quiz(quiz_id) ON DELETE CASCADE NOT NULL,
    text TEXT NOT NULL
);

CREATE TABLE survey_answer(
  survey_answer_id SERIAL PRIMARY KEY,
  survey_question_id INT REFERENCES survey_question(survey_question_id) ON DELETE CASCADE NOT NULL,
  number INT NOT NULL,
  text TEXT NOT NULL,
  emoji TEXT NOT NULL
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

-------------------  WELCOME QUIZ  ---------------------

INSERT INTO quiz(quiz_info, quiz_intro_message, receive_role_after_finish)
VALUES ('welcome quiz', 'ahoj toto je welcome quiz bla bla bla.. smajliky ber s rezervou', 'member');


INSERT INTO survey_question(quiz_id, text)
VALUES(1, 'Pohlavie');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(1, 1, 'Muž', '🦸‍♂️');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(1, 2, 'Žena', '🦸‍♀️');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(1, 3, 'Iné', '⚪');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(1, 4, 'Nechcem odpovedať', '❔');


INSERT INTO survey_question(quiz_id, text)
VALUES(1, 'Vek');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 1, '0 - 17', '👶');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 2, '18 - 22', '🧑‍🦱');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 3, '23 - 27', '👱‍♀️');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 4, '28 - 34', '🧔');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 5, '35 a viac', '👨‍🦲');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 6, 'Nechcem odpovedať', '❔');

INSERT INTO survey_question(quiz_id, text)
VALUES(1, 'Ako si na tom s programovaním?');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(3, 1, 'Chcem sa naučiť programovať', '🤓');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(3, 2, 'Už viem niečo naprogramovať', '🥳');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(3, 3, 'Pracujem ako programátor', '😎');

INSERT INTO survey_question(quiz_id, text)
VALUES(1, 'Počúvaš naše podcasty?');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(4, 1, 'Počul/a som jednu alebo dve epizódy', '🙂');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(4, 2, 'Viac ako 2 epizódy', '😋');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(4, 3, 'Zatiaľ nie', '🥲');

INSERT INTO survey_question(quiz_id, text)
VALUES(1, 'Aký obsah by si od nás privítal/a najčastejšie?');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(5, 1, 'Podcasty', '🎙️');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(5, 2, 'Videá o programovaní', '📷');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(5, 3, 'Články o programovaná', '📝');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(5, 4, 'Kurzy o programovaní', '🎥');

INSERT INTO survey_question(quiz_id, text)
VALUES(1, 'Môžeme ti v budúcnosti posielať takéto krátke dotazníky?');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(6, 1, 'Áno', '👍');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(6, 2, 'Nie, ďakujem', '👎');