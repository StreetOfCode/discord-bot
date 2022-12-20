DELETE FROM survey_question WHERE survey_id=4;
DELETE FROM survey WHERE survey_id=4;

SELECT setval('survey_survey_id_seq', 3);
SELECT setval('survey_question_survey_question_id_seq', 19);
