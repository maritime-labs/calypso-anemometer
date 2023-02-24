$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval black        := $(venv)/bin/black)
$(eval isort        := $(venv)/bin/isort)
$(eval pytest       := $(venv)/bin/pytest)
$(eval twine        := $(venv)/bin/twine)
$(eval ruff         := $(venv)/bin/ruff)
$(eval proselint    := $(venv)/bin/proselint)

setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venv) || python -m venv $(venv)
	@$(pip) install --quiet --requirement=requirements-utils.txt

format: setup-virtualenv
	$(black) .
	$(isort) .
	$(ruff) --fix --ignore=ERA --ignore=F401 --ignore=F841 --ignore=T20 .

lint: setup-virtualenv
	$(ruff) check .
	$(black) --check .
	$(isort) --check .
	$(MAKE) proselint

proselint:
	$(proselint) *.rst doc/**.rst

test: setup-virtualenv
	$(pip) install --editable=.[test,fake]
	$(pytest)

publish: setup-virtualenv
	$(pip) install build twine
	$(python) -m build
	$(twine) upload --skip-existing --verbose dist/*{.tar.gz,.whl}
