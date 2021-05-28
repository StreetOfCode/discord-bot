ALTER TABLE survey ADD COLUMN channel_name_suffix TEXT NOT NULL DEFAULT '';

INSERT INTO survey(survey_info, survey_intro_message, channel_name_suffix)
VALUES ('podcast feedback survey',
        E'Ahoj, ja som Street of Code bot a chcem sa ťa opäť spýtať pár otázok. Tvoje odpovede ako vždy vidia iba admini.\n\nCieľom tohto dotazníka je získať feedback k podcastom.\n\nSmajlíky ber prosím s rezervou. Ďakujem :)',
        'podcast-feedback'
       );

-- Watch out for correct ids on survey_id and survey_question_id
-- Last survey had id 1, so this new will have id 2.
-- Last survey_question had id 7, so next one will have id 8

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(2, 1, 'Vadí ti tykanie v našom podcaste?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(8, 1, 'Vadí mi to', '😡');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(8, 2, 'Nevadí mi to', '🙂');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(8, 3, 'Je mi to jedno', '😑');


INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(2, 2, 'Ako sa ti páči naša intro hudba v podcaste?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(9, 1, 'Vôbec', '🤮');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(9, 2, 'Je to ok', '🙂');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(9, 3, 'Je úplne top', '🤩');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(9, 4, 'Aká hudba?', '😱');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(9, 5, 'Neviem', '🙄');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(2, 3, 'Čo si myslíš o dĺžke našich epizód?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(10, 1, 'Epizóda je často príliš dlhá', '🧐');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(10, 2, 'Epizóda môže byť pokojne aj dlhšia', '😇');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(10, 3, 'Vyhovuje mi to', '🙂');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(10, 4, 'Je mi to jedno', '😑');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(10, 5, 'Neviem', '🙄');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(2, 4, 'Čo si myslíš o štruktúre našich epizód?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(11, 1, 'Vyhovovalo by mi, keby to bolo viac organizované', '🧐');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(11, 2, 'Vyhovovalo by mi, keby to bolo viac uvoľnené', '🤪');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(11, 3, 'Je to dobré ako to je', '🙂');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(11, 4, 'Je mi to jedno', '😑');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(11, 5, 'Neviem', '🙄');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(2, 5, 'Ako hodnotíš kvalitu audia v našich epizódach?', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(12, 1, 'Kvalita by mohla byť lepšia', '🤨');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(12, 2, 'Nevšimol/la som si, že by mi niečo vadilo', '🙂');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(12, 3, 'Kvalita je podľa mňa dobrá', '🤩');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(12, 4, 'Je mi to jedno', '😑');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(12, 5, 'Neviem', '🙄');

INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(2, 6, 'Odpovedal/a si na všetky otázky? Ked pridáš 👍, tak tieto odpovede už nebudeš môcť meniť a dokončíš dotazník.', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(13, 1, 'Áno', '👍');