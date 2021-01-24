## `/send-welcome-survey`

Sends the welcome survey to users, who are present on the server but for some reason haven't received the welcome survey
automatically.

## `/ping-unanswered-survey`

Pings (notifies) users who haven't completed a survey for longer than `PING_UNANSWERED_SURVEY_OLDER_THAN`.

## `/delete-finished-surveys-channels`

Deletes channels of surveys, which have been finished for more than `DELETE_FINISHED_SURVEYS_OLDER_THAN`.