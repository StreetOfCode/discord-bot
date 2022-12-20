INSERT INTO survey(survey_info, survey_intro_message, channel_name_suffix)
VALUES ('social media survey', 'Prišiel čas na ďalšie drahocenné zbieranie informácii. Tentoraz by sme sa radi dozvedeli o tvojich preferenciách, čo sa týka sociálnych sietí. Pomôže nám to sa rozhodnúť, do ktorých sociálnych sietí by sme mali vkladať najväčšiu snahu, a naopak ktoré nás nemusia zaujímať. Ďakujeme!', 'social-media');

-- Watch out for correct ids on survey_id and survey_question_id
-- Last survey had id 3, so this new will have id 4.
-- Last survey_question had id 19, so next one will have id 20

-- question id 20
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(4, 1, 'Odkiaľ si sa o nás dozvedel/a?', FALSE, FALSE);

INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(20, 1, 'Odporučíl mi vás známy/a', '🤩');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(20, 2, 'Cez podcast, na ktorý som narazil/a náhodne', '🎙️');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(20, 3, 'Zobrazili ste sa na Googli, keď som niečo hľadal/a', '💻');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(20, 4, 'Cez sociálne siete', '😉');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(20, 5, 'Nepamätám si / Neviem', '🥱');

-- question id 21
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(4, 2, 'Aké sociálne siete používaš?', TRUE, FALSE);

INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(21, 1, 'Instagram', '1️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(21, 2, 'Facebook', '2️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(21, 3, 'Twitter', '3️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(21, 4, 'TikTok', '4️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(21, 5, 'Linkedin', '5️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(21, 6, 'Žiadne', '🥱');

-- question id 22
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(4, 3, 'Na akých sociálnych sieťach nás sleduješ?', TRUE, FALSE);

INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(22, 1, 'Instagram', '1️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(22, 2, 'Facebook', '2️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(22, 3, 'Twitter', '3️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(22, 4, 'Nikde', '🥱');

-- question id 23
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(4, 4, 'Odkiaľ by si sa najradšej dozvedel/a novinky o našej tvorbe?', FALSE, FALSE);

INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(23, 1, 'Discord', '1️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(23, 2, 'Newsletter (pridať sa môžeš na streetofcode.sk/newsletter)', '2️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(23, 3, 'Instagram', '3️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(23, 4, 'Linkedin', '4️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(23, 5, 'Facebook', '5️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(23, 6, 'TikTok', '6️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(23, 7, 'Je mi to jedno', '🥱');

-- question id 24
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice, is_open_ended)
VALUES(4, 5, 'Kde najviac počúvaš náš podcast?', FALSE, FALSE);

INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(24, 1, 'Priamo cez vašu stránku', '👌');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(24, 2, 'Spotify', '1️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(24, 3, 'YouTube', '2️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(24, 4, 'Apple Podcasts', '3️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(24, 5, 'Google Podcasts', '4️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(24, 6, 'Cez inú aplikáciu', '5️⃣');
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(24, 7, 'Nepočúvam váš podcast', '🥱');

-- question id 25
INSERT INTO survey_question(survey_id, _order, text, is_multiple_choice)
VALUES(4, 6, 'Odpovedal/a si na všetky otázky? Ked pridáš 👍, tak tieto odpovede už nebudeš môcť meniť a dokončíš dotazník.', FALSE);
INSERT INTO survey_answer(survey_question_id, _order, text, emoji)
VALUES(25, 1, 'Áno', '👍');
