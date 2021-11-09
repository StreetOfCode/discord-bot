# Prerequisites
1. Access to Heroku `discord-soc-bot` app
2. Heroku git remote setup (see [docs](https://devcenter.heroku.com/articles/git))
3. GitHub repository write access

# Steps
1. Merge all PRs you wish to deploy into `develop` branch.
2. Fetch and checkout `develop` branch.
3. Find production `DATABASE_URL` in Heroku.
4. Make a backup of the DB just in case anything goes wrong:
```
pg_dump [DATABASE_URL] > dbBackup[DATE].sql
```
e.g.
```
pg_dump postgresql://discordbot:somePassword@localhost/discord_bot > dbBackup20211109.sql
```
5. If DB schema has been updated continue with step 6. Otherwise you can skip to step 8.
6. Change `yoyo-local.ini` `database` to the `DATABASE_URL` from Heroku.
7. Run yoyo migrations:
```
pipenv run yoyo apply
```
8. After applying the migrations carefully check logs if everything went OK. If possible, connect to the DB and check if its tables were updates as expected.
9. Set `master` branch to track `develop` branch:
```
git checkout develop
git branch -f master
```
10. Push new `master` to GitHub repo:
```
git push origin master
```
11. Open Heroku logs:
```
heroku logs --tail -a discord-soc-bot
```
12. Open a second terminal (keep the one with the logs) and push `master` to Heroku:
```
git push heroku master
```
13. Check the logs if everything went OK.
14. Test some basic functionality e.g. `/show-stats` command.
15. Feel free to marvel at your awesomeness.