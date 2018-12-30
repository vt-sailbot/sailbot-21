ROOT_DIR = $(shell pwd)

init:
	pip install virtualenv; \
	virtualenv -p python3.7 p3_7env --no-site-packages; \
	source ./p3_7env/bin/activate; \
	pip install -r requirements.txt; \
	cd src/msg && $(MAKE) build
	-mkdir bin
	cd $(ROOT_DIR)/tests/msg_tests && $(MAKE) build ROOT_DIR=$(ROOT_DIR)

test:
	cd tests/msg_tests && $(MAKE) test ROOT_DIR=$(ROOT_DIR)
	source ./p3_7env/bin/activate; \
	export ENV test; \
	python -m unittest discover -vcs tests

clean:
	cd src/msg && $(MAKE) build

.PHONY: init test clean
