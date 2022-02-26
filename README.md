# discord-bot

## Setup

### Development environment

We're using Python 3.9.

Install [pipenv](https://pipenv.pypa.io/en/latest/install/).

Execute:

```
pipenv install
```

### Database

Setup a PostgreSQL database server locally. Create a database for the Discord bot. Copy `yoyo-local.ini.template` to `yoyo-local.ini`:
```
cp yoyo-local.ini.template yoyo-local.ini
```

Set the `database` variable in that file and run migrations:
```
yoyo apply
```

### Environment variables

Copy `.env.template`:

```
cp .env.template .env
```

Fill in the missing values. Don't forget db `USER` and `PASSWORD`.

The `*_OLDER_THAN` variables use the PostgreSQL [interval](https://www.postgresql.org/docs/9.1/functions-datetime.html)
type. E.g:

- `1 day`
- `30 seconds`
- `3 hours`

### Discord

- Create a discord server.
- Go to [https://discord.com/developers](https://discord.com/developers) and create a new application
- Enable `SERVER MEMBERS INTENT` in `Settings` -> `Bot`
- Enable the `bot` scope in `OAuth2` -> `SCOPES`, enable `BOT PERMISSIONS` -> `Administrator` and then navigate to the
  URL which reveals itself and add the bot to your server
- Navigate back to applications, copy the bot `TOKEN` from `SETTINGS` -> `Bot` and paste it into your `.env` file
- Create a `administrator` role on your server and fill its ID into the `ADMINISTRATOR_ROLE_ID` environment variable

## Running locally

That's it. You can now start the bot by running:

```
python src/main.py
```

## Contributing

We will gladly accept contributions, but before you start working on something please
read [CONTRIBUTING.md](docs/CONTRIBUTING.md) first.
