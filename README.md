# discord-bot

## Setup

Install [pipenv](https://pipenv.pypa.io/en/latest/install/).

Run:

```
pipenv shell
pipenv install
```

Setup a PostgreSQL database. Run `init_db.sql`.

Copy `.env.template`:

```
cp .env.template .env
```

Fill in the missing values. Don't forget db `USER` and `PASSWORD`.

That's it. Let the bitch run!
