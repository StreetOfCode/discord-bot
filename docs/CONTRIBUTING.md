Before starting work on some new feature/bug fix please create an Issue in our GitHub repository and describe, what you
are planning or what the issue is. There we can discuss if what you are proposing is something we would like to add and
what the best way to do that is.

## Review process

- File a Pull Request (PR) with a number of well-defined clearly described commits (following what is described
  in [this article](https://chris.beams.io/posts/git-commit/) is a good start). Multiple commits per PR are allowed, but
  please do not include revert commits, etc. Use rebase.
- Make sure that the code is well formatted - use `iSort` and `Black` for that:

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