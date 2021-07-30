## `/send-welcome-survey`

Sends the welcome survey to users, who are present on the server but for some reason haven't received the welcome survey
automatically.

## `/ping-unanswered-survey`

Pings (notifies) users who haven't completed a survey for longer than `PING_UNANSWERED_SURVEY_OLDER_THAN`.

## `/delete-finished-surveys-channels`

Deletes channels of surveys, which have been finished for more than `DELETE_FINISHED_SURVEYS_OLDER_THAN`.

## `/delete-unanswered-surveys-channels`

Deletes channels of surveys, which have been unanswered for more than `DELETE_UNANSWERED_SURVEYS_OLDER_THAN`.

## `/create-channel-teams {channel_id} {number_of_teams}`

Creates balanced teams with users in given channel_id

## `/send-survey {surve_id}`

Sends survey (id of survey in first parameter) to all users who are survey-fans


## `/clear-show-stats-cache`

Deletes all rows from show_stats_cache db table. Useful when there are breaking changes in show_stats command