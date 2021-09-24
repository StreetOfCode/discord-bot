ALTER TABLE survey_question DROP COLUMN is_open_ended;
ALTER TABLE user_survey_answer DROP COLUMN text;
ALTER TABLE user_survey_answer DROP COLUMN message_id;
ALTER TABLE user_survey_answer ALTER COLUMN survey_answer_id SET NOT NULL;
