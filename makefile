.PHONY: docs

all: unittest

docs:
	cd docs && make html

unittest:
	coverage run --source=april setup.py test

clean:
	find . -name "*.pyc" -exec rm -f {} \;
