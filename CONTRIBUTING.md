# Contributing

Thank you for wanting to contribute to this project!

The following elements will allow you to contribute with a little guide
to learn how to make an approved contribution. Don't hesitate to share
some new ideas to improve it!

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting started](#getting-started)
  - [Pre-requisites](#pre-requisites)
  - [Clone the repository](#clone-the-repository)
  - [Environment setup](#environment-setup)
- [How to contribute?](#how-to-contribute)
  - [Organization](#organization)
    - [Report issues](#report-issues)
    - [Work on issues](#work-on-issues)
    - [Pull Requests](#pull-requests)
    - [Release](#release)
  - [Writing code](#writing-code)
    - [References](#references)
    - [Quality Assurance](#quality-assurance)
      - [Development method](#development-method)
      - [Lint](#lint)
      - [Tests](#tests)
      - [Security](#security)
      - [Documentation](#documentation)
  - [Git](#git)
    - [Ignore](#ignore)
    - [Hooks](#hooks)
    - [Pull](#pull)
    - [Branches](#branches)
    - [Commit](#commit)
      - [Types](#types)
      - [Scopes](#scopes)
      - [Subject](#subject)

## Code of Conduct

When you are contributing, keep in mind to:

- Remain respectful of different points of view and experiences.
- Accept constructive criticism.
- Show sympathy for other contributors.

## Getting started

### Pre-requisites

We recommended a linux-based distribution. You will need the following
tools on your system:

- [Git](https://git-scm.com/)
- [Make](https://www.gnu.org/software/make/)
- [Python](https://www.python.org/)
- [Virtualenv](https://virtualenv.pypa.io/)

### Clone the repository

```bash
git clone https://github.com/CGuichard/pffmpeg
```

### Environment setup

First, create an isolated Python virtual environment:

```bash
virtualenv -p python3.10 .venv
source .venv/bin/activate
pip install --upgrade pip
# OR
python3.10 -mvenv --upgrade-deps .venv
source .venv/bin/activate
```

List available commands:

```bash
make help
```

You must also install in editable mode, with dev dependencies.

```bash
make install-dev
```

This project uses multiple tools for its development, and your virtual
environment created earlier is just here to give you a working
development environment. Some tools are handled in sub-virtual
environments created by [Tox](https://tox.wiki), a virtual env manager
and automation tool. The `install-dev` only gives you the tools that you
will be directly using, delegating other installations inside of *Tox*
virtual envs.

In order to complete the environment setup, you must install some Git
Hooks. You can refer to the dedicated section of this document: [Hooks](#hooks).

## How to contribute?

### Organization

#### Report issues

Traceability is necessary for a healthy development environment. Each
bug encountered must be reported with the creation of an issue. Details
on how to reproduce it must be provided, and if possible visuals
(screenshots) are welcome.

There are two kinds of issue:

- [Bug Report](https://github.com/CGuichard/pffmpeg/issues/new?template=bug_report.md)
- [Feature Request](https://github.com/CGuichard/pffmpeg/issues/new?template=feature_request.md)

Click on these links to visit the issue creation page, with a simple
template to guide you.

Please, remember that a title isn't enough for an issue.

#### Work on issues

You can work on every open issue. Keep in mind to reference them in your
commits and pull requests, by following the [GitHub convention](https://docs.github.com/en/github/writing-on-github/autolinked-references-and-urls#issues-and-pull-requests).

You must work on a separate branch for each issue. Check out
the [branch naming convention](#branches).

#### Pull Requests

Please follow these guidelines:

- Use a clear and descriptive title.
- Include every relevant issue number in the body, not in the title.
- Give a complete description of every change made in the body.

If a branch is merged and no longer needed, make sure it was closed.

#### Release

You can create a release with `make release`. Because we follow a
[commit convention](#commit), the next version is guessed from
the commit history. The `CHANGELOG.md` is generated automatically too.

Don't forget to push the tags to your origin repo!

```bash
git push --tags
```

### Writing code

#### References

Writing clean code is very important for a project. References such as
"Clean Code", by Robert C. Martin, are good to keep in mind. Readable
code is not a luxury, it is a necessity.

Let us be reminded of the Zen of Python, by Tim Peters:

```text
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

You are not alone for this difficult task. In the next sections you will
find about our recommended development method, our linting and
formatting tools, and how to use tests.

#### Quality Assurance

##### Development method

The favored method of development will be TDD (Test Driven Development).

The TDD process can be explained like this:

1. Add a test.
2. Run all tests. The new test should fail for expected reasons
    (failing by compilation error doesn't count as true failing, you
    must be able to compile your code).
3. Write the simplest code that passes the new test.
4. All tests should now pass.
5. Refactor as needed, using tests after each refactors to ensure that
    functionality is preserved

Repeat...

##### Lint

To ensure good code writing, we use a lot of lint tools:

- [validate-pyproject](https://validate-pyproject.readthedocs.io):
    command line tool and Python library for validating
    `pyproject.toml`, includes models defined for `PEP 517`, `PEP 518`
    and `PEP 621`.
- [ruff](https://docs.astral.sh/ruff/): an extremely fast Python linter and formatter,
    written in Rust. Integrate `pyupgrade`, `pylint`, `bandit`, `isort`,
    `eradicate`, and `flake8` with dozens of its plugins.
- [mypy](https://mypy.readthedocs.io): static type checker.

These tools are run with:

```bash
make lint
```

You can use `lint-watch` to run ruff on `src/` with `--watch` flag. This
is really useful as it gives you instantaneous feedback on your code.

> Note: All of these are also run for each commit, failing the commit
> if at least one error is found.

##### Tests

We shall always aim for the highest code coverage in our tests, and our
development environment should use tools that will help us ensure it.

The test frameworks used are unittest and pytest, run with tox. Thanks
to pytest-cov, code coverage is evaluated and fails under 90% of test
coverage.

Run the tests with *make*:

```bash
make test
```

> Note: Tests are run before each push, failing the push if it fails.

##### Security

We use [pip-audit](https://pypi.org/project/pip-audit/) to check our Python
dependencies for potential security vulnerabilities and suggests the
proper remediations for vulnerabilities detected.

```bash
make security
```

> Note: Security check is run before each push, failing the push if it fails.

##### Documentation

Doing features is great, but it is useless if nobody knows how to use
them. Keeping a clean, up-to-date documentation is of high priority.

This project is documented with [MkDocs](https://www.mkdocs.org/).
The documentation source can be found in the `docs/src` folder.

You can build the docs with:

```bash
make docs
```

If you want to build the docs, and serve it with an http server after
the build:

```bash
make docs serve
```

When writing the docs, use the live server to automatically rebuild the
docs.

```bash
make docs-live
```

### Git

#### Ignore

When you want to hide something from Git's all-seeing eyes, don't
stubbornly use the `.gitignore` file. There are three native ways in Git
to ignore files/folders:

1. `.gitignore`: Patterns that should be version-controlled and
    distributed to other repositories via clone (i.e., files that all
    developers will want to ignore), to put it bluntly, non-tracked
    files generated by the project lifecycle can be put here.
2. `.git/info/exclude`: Patterns that are specific to a particular
    repository but which do not need to be shared with other related
    repositories (e.g., auxiliary files that live inside the repository
    but are specific to one user's workflow).
3. Patterns which a user wants Git to ignore in all situations (e.g.,
    backup or temporary files generated by the user's editor of choice)
    generally go into a file specified by `core.excludesFile` in the
    user's `~/.gitconfig`.

More details in the full *official* documentation of Git
[here](https://git-scm.com/docs/gitignore).

To summarize, don't write in the `.gitignore` files generated by your
workflow if it is not common to all developers on the project. To serve
that purpose, mandatory tools must be specified in this section.

*There is no mandatory IDE/tool at the moment.*

#### Hooks

We use [Pre-commit](https://pre-commit.com/) to run tools at specific
moments of the Git workflow, with [Git Hooks](https://git-scm.com/docs/githooks).
It will mostly run linting and formatting tools on the source code in our case.
Some tools will also run for yaml, json, or markdown files etc... The commitizen
tool will also enforce conventional commit usage, that will ne discussed in
the [Commit](#commit) section.

To activate our Git Hooks, please run the following commands:

```bash
pre-commit install --install-hooks
```

Our hooks needs the following dependencies:

- Python (>=3.10)
- pre-commit (~=3.7)

#### Pull

It is good practice to pull with rebase over a normal pull.

```bash
git switch <your-branch>

# classic
git pull

# much better
git pull --rebase
```

But do keep in mind that to be able to rebase, you'll need to have a
clean state of your repository, with no changes to commit. If that's not
the case, you can use `stash` in addition:

```bash
git switch <your-branch>
git stash
git pull --rebase
git stash pop
```

If you don't want to specify `--rebase` each time you pull, configure it:

```bash
git config --local pull.rebase true
```

And if you don't want to manually `stash` at each rebase, you can also
configure it:

```bash
git config --local rebase.autostash true
```

Now each `git pull` will use `--rebase` and automatically `stash`!

#### Branches

Here's our branch naming convention:

- Immutable branches:
  - `main`: our main branch, must have no error.
  - `develop`: branch used to work, where you merge your work
        branches.
- Work branches:
  - `<scope>/<short-name>`: you work here.

List of scopes:

- **fix**: fix a bug
- **feat**: add a feature
- **docs**: documentation changes
- **refactor**: code refactoring

Those are examples, if you come up with other scopes, you can use them.
You can also use a scope from our commit convention as a branch scope.

We will prefer the use of "-" over "\_".

Example:

```bash
git checkout -b fix/sanitize-paths
```

Don't forget to delete your local branches when you don't need them
anymore.

```bash
git branch -d <branch-name>
```

To keep your local refs to remote branches clean, use:

```bash
git remote prune origin
```

Here's one process that you can follow once your local branch was
pushed, successfully merged into `main`, and if you don't need it
anymore:

```bash
git switch main
git pull
git branch -d <my-branch>
git remote prune origin
```

You can also use a scope from our commit convention as a branch scope.

#### Commit

Based on [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

Summary :

```text
<type>(<scope>): <subject>
```

The scope is optional, you can find a simpler form:

```text
<type>: <subject>
```

In order to be concise, type and scope should not be longer than 10
characters. Limit the first line to 70 characters or less.

##### Types

- **build:** Changes that affects the build system or external dependencies,
  such as adding a dependency, or modifying the build system.
- **bump:** version change, new release.
- **ci:** Changes in CI.
- **chore:** Changes which does not modify the code sources nor the tests.
- **docs:** Addition or modification of documentation/comment.
- **feat:** Adding or modifying a feature.
- **fix:** Bug fix.
- **perf:** Code change that improves performance.
- **refactor:** Code change that doesn't fix a bug or add a feature.
- **revert:** Rollback changes from a previous commit.
- **style:** Changes that does not affect the sense/meaning of the
  code (space, formatting, semicolon, newline, etc...).
- **test:** Addition of missing tests or correction of existing tests.

##### Scopes

This part is optional, it can be used to define more precisely what is
impacted. Examples:

```text
build(wheel): add x to the wheel
refactor(modulename): change x in y class
```

##### Subject

This is the content of your commit message. Please follow these rules:

- It starts with a lowercase letter.
- It does not end with a point.
- It must be conjugated in the imperative.
- The message should explain the what and the why, but not how.

```bash
git commit -m "type(scope): message"
```

If you need a longer message, you can add a "body" to the commit.

```bash
git commit
```

Git then opens an editor to write the commit.

```text
type(scope): message

I am the body of the commit and I am not limited in size.
However, keep in mind that if the commit needs a large description it may be better to have an issue with it.
```
