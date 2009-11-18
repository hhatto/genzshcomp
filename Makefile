
all: tests

tests:
	ls

pypireg:
	python setup.py register
	python setup.py sdist bdist_egg upload

clean:
	rm *.pyc
