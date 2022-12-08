## Lint your code using pylint
.PHONY: lint
lint:
	python -m pylint --version
	python -m pylint src
## Run tests using pytest
.PHONY: test
test:
	python -m pytest --version
	python -m pytest yt_watch_history_analyzer/tests
## Format your code using black
# .PHONY: black
# black:
# 	python -m black --version
# 	python -m black .## Run ci part
.PHONY: ci
	ci: precommit lint test

.PHONY: install
install: 
	pip install -U .

.PHONY: image
install: 
	docker build . 

venv:
 pip install pip-tools
 pip-compile requirements.in
 pip install -r requirements.txt

check_compile:
 pip-compile --quiet requirements.in && git diff --exit-code
 
build: | venv
 pip install setuptools wheel
 python setup.py sdist bdist_wheel