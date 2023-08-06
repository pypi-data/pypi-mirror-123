# dep-appearances

A simple tool to see where your dependencies are imported.  The `dep-appearances`
CLI produces a report of which files import each of your dependencies.  At this
time, the CLI only works for projects that use
[`pipenv`](https://pipenv.pypa.io/en/latest/), but support for any dependency
management tool could be added.

## Requirements

* Python 3

## How to Use dep-appearances

You can install `dep-appearances` via `pip`:

```
pip install dep-appearances
```

Installing the package provides a CLI:

```
dep-appearances --help
usage: dep-appearances [-h] [--underused_threshold UNDERUSED_THRESHOLD] [PATH]

Find dependencies that are unused and underused in your codebase.

positional arguments:
  PATH                  The path to your project's root (defaults to your
                        current working directory)

optional arguments:
  -h, --help            show this help message and exit
  --underused_threshold UNDERUSED_THRESHOLD
                        The threshold to set for marking dependencies as
                        underused (default: 2)
```

From the root of your project (i.e. wherever your `Pipfile` is) you can run
`dep-appearances` and you will get a report of dependencies that don't appear to
imported _and_ a report of dependencies that my not be imported in very many
places.

```
> dep-appearances
Unused dependencies:
	build
	pytest
	twine

Underused dependencies (usage threshold = 2):
	pipfile
		imported in:
		src/dep_appearances/appearances_report.py:3
```

### Known Shortcomings

There are, unfortunately, packages that have a different name when importing
them than when installing them.  For example, the `apache-airflow` package shows
up in a Pipfile as `apache-airflow`, but when it is used in a codebase you use

```
import airflow
```

`dep-appearances` currently does **not** account for such cases.  Therefore
you should not remove dependencies from your codebase without confirming that
packages are unused.

## How to contribute to dep-appearances

Pull requests are definitely welcome.  Just fork this repo and open a PR
against the `main` branch.

### Useful Development Commands

Install dependencies

```
pipenv install
```

Install and use the package locally (to work on the CLI):

```
pipenv run pip install -e .
pipenv run dep-appearances
```

Running tests:

```
pipenv run pytest
```

## Release Process

```
# Generate distribution archives:
python3 -m build
# => Should create files in dist/

# Push to pypi
python3 -m twine upload dist/*
```

### Building for test.pypi


```
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```

Install from test.pypi:

```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps dep-appearances
```
