
all: tests

tests:
	python test/test_genzshcomp.py

pypireg:
	python setup.py register
	python setup.py sdist bdist_egg upload

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm *.pyc
