$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval black        := $(venv)/bin/black)
$(eval isort        := $(venv)/bin/isort)
$(eval pytest       := $(venv)/bin/pytest)
$(eval twine        := $(venv)/bin/twine)
$(eval flake8       := $(venv)/bin/pflake8)

setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venv)

format: setup-virtualenv
	$(pip) install --requirement=requirements-utils.txt
	$(black) .
	$(isort) .

lint: setup-virtualenv
	$(pip) install --requirement=requirements-utils.txt
	$(flake8) calypso_anemometer examples testing

test: setup-virtualenv
	$(pip) install --editable=.[test,fake]
	$(pytest)

publish: setup-virtualenv
	$(pip) install build twine
	$(python) -m build
	$(twine) upload --skip-existing --verbose dist/*{.tar.gz,.whl}
