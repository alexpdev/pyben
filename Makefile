.PHONY: clean docs help push release dist install lint
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr **/.pytest_cache
	rm -fr *.egg-info
	rm -fr *.egg
	rm -f **.pyc
	rm -f **.pyo
	rm -f **~
	rm -fr **/__pycache__
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -f corbertura.xml
	rm -f coverage.xml
	rm -fr .codacy-coverage

lint: ## check style with flake8
	black pyben
	black tests
	isort pyben
	isort tests
	prospector pyben
	prospector tests

test: ## run tests quickly with the default Python
	pytest tests --cov=tests --cov=pyben --pylint

push: lint docs clean test
	git add .
	git commit -m "$m"
	git push
	coverage run --source pyben -m pytest tests
	coverage xml -o coverage.xml
	bash codacy.sh report -r coverage.xml
	rm coverage.xml

docs: ## generate Sphinx HTML documentation, including API docs
	rm -rf docs
	mkdocs build
	touch docs/.nojekyll

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	python setup.py bdist_egg
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

build: lint test docs clean ## Build project library
	python setup.py sdist
	python setup.py bdist_wheel
	python setup.py bdist_egg
