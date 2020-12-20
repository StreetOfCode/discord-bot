DROP TABLE IF EXISTS test;
CREATE TABLE test(id SERIAL PRIMARY KEY, test TEXT);
-- real TABLES
DROP TABLE IF EXISTS survey_question CASCADE;
CREATE TABLE survey_question(survey_question_id SERIAL PRIMARY KEY, text TEXT);
DROP TABLE IF EXISTS survey_answer CASCADE;
CREATE TABLE survey_answer(
  survey_answer_id SERIAL PRIMARY KEY,
  survey_question_id INT REFERENCES survey_question(survey_question_id) ON DELETE CASCADE,
  number INT,
  text TEXT,
  emoji TEXT
);
DROP TABLE IF EXISTS sent_survey_question CASCADE;
CREATE TABLE sent_survey_question(
  sent_survey_question_id SERIAL PRIMARY KEY,
  user_id BIGINT,
  survey_question_id INT,
  message_id BIGINT
);
DROP TABLE IF EXISTS user_survey_answer CASCADE;
CREATE TABLE user_survey_answer(
  user_id BIGINT,
  survey_question_id INT REFERENCES survey_question(survey_question_id) ON DELETE CASCADE,
  survey_answer_id INT REFERENCES survey_answer(survey_answer_id) ON DELETE CASCADE
);
INSERT INTO survey_question(text)
VALUES('Uroven?');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(1, 1, 'Stazista (ucim sa)', '⏹');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(1, 2, 'Junior', '👶');
INSERT INTO survey_question(text)
VALUES('Nejaka dalsia otazka');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 1, 'Otaznik', '❓');
INSERT INTO survey_answer(survey_question_id, number, text, emoji)
VALUES(2, 2, 'Vykricnik', '❗');
