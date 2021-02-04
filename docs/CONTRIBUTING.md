Before starting work on some new feature/bug fix please create an Issue in our GitHub repository and describe, what you
are planning or what the issue is. There we can discuss if what you are proposing is something we would like to add and
what the best way to do that is.

## Database migrations

We are using [yoyo-migrations](https://pypi.org/project/yoyo-migrations/) for database migraitons. To create a new
migration use:

```
yoyo new --sql
```

Name the file similarly to `xxxx.[migration_name].sql` where `xxxx` is the next migration number. Write your SQL
statements into that file. Also create a `xxxx.[migraiton_name].rollback.sql` file which will contain the commands for,
well, migration rollback. Run the following command to apply your migration:

```
yoyo apply
```

## Review process

- File a Pull Request (PR) with a number of well-defined clearly described commits (following what is described
  in [this article](https://chris.beams.io/posts/git-commit/) is a good start). Multiple commits per PR are allowed, but
  please do not include revert commits, etc. Use rebase.
- Make sure that the code is well formatted - use `iSort` and `Black` for that. You can either setup your editor to use
  them or run:

```
pipenv shell
isort src
black src
```

- Assign both [gabrielkerekes](https://github.com/gabrielKerekes) and [xjahic](https://github.com/xjahic) as reviewers.
- When addressing code review comments please
  use _[fixup](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---fixupltcommitgt)_ commits:

```
git commit --fixup HEAD
```

or some older commit:

```
git commit --fixup fe4fec5
```

- Reply directly to the review comments and add a link to the fixup commit which addressed that comment.
- After the PR is approved, use `git rebase -i [PARENT_BRANCH] --autosquash`. This will squash the fixup commits.
- One of the reviewers will merge the PR.
