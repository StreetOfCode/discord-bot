INSERT INTO survey(survey_info, survey_intro_message, channel_name_suffix)
VALUES ('podcast topics survey', 'Serus 🤙 Zbierame nápady na témy do podcastu alebo na videá. Taktiež by sme chceli vedieť feedback k existujúcim epizódam. Ďakujeme!', 'podcast-topics');

-- Watch out for correct ids on survey_id and survey_question_id
-- Last survey had id 2, so this new will have id 3.
-- Last survey_question had id 13, so next one will have id 14

-- question id 14
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(3, 1, E'Epizódy o programovaní vs. epizódy o živote ako takom - čo sa ti viac páči?', FALSE, FALSE);

INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(14, 1, 'Chcel/a by som počuť viac epizód o programovaní', '💻');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(14, 2, 'Chcel/a by som počuť viac epizód o živote ako takom', '🧬');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(14, 3, 'Páči sa mi ako to máte - prevažne o programovaní a sem tam o živote ako takom', '👍');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(14, 4, 'Niečo iné', '🤔');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(14, 5, 'Neviem', '🤷‍♂️');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(14, 6, 'Je mi to jedno', '🥱');

-- question id 15
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(3, 2, E'Epizódy s hosťami', FALSE, FALSE);

INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(15, 1, 'Chcel/a by som, aby ste mali v epizódach častejšie hosťa na danú tému', '👌');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(15, 2, 'Vyhovuje mi, keď raz za čas budete mat v podcaste hosťa', '👍');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(15, 3, 'Nevyhovuje mi, keď máte v podcaste hosťa', '🚷');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(15, 4, 'Neviem', '🤷‍♂️');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(15, 5, 'Je mi to jedno', '🥱');

-- question id 16
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(3, 3, E'Aké epizódy sa ti zatiaľ najviac páčili? Skús si prosím spomenúť o čom boli, alebo ako sa volali', FALSE, TRUE);

-- question id 17
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(3, 4, E'Akých hosťov (z akých odborov) by si chcel/a počuť v podcaste?', FALSE, TRUE);

-- question id 18
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(3, 5, E'Máš niečo, k čomu by si chcel/a počuť náš názor? Je niečo, čo sme už dávno mali prebrať, ale ešte sme tak neurobili? Nerozumieš nejakej téme a myslíš si, že by ti mohla nejaká epizódka alebo video pomôcť?', FALSE, TRUE);

-- question id 19
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(3, 6, 'Odpovedal/a si na všetky otázky? Ked pridáš 👍, tak tieto odpovede už nebudeš môcť meniť a dokončíš dotazník.', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(19, 1, 'Áno', '👍');
