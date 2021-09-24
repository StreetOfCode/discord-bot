ALTER TABLE survey_question ADD COLUMN is_open_ended BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE user_survey_answer ADD COLUMN text TEXT DEFAULT NULL;
ALTER TABLE user_survey_answer ADD COLUMN message_id BIGINT DEFAULT NULL;
ALTER TABLE user_survey_answer ALTER COLUMN survey_answer_id DROP NOT NULL;
