.PHONY: install test-install test clean

venv:
	python3 -m venv venv

install: venv
	. venv/bin/activate; pip install -r requirements.txt

test-install: install
	. venv/bin/activate; pip install -r tests/requirements.txt

test:
	. venv/bin/activate; pytest tests

clean:
	rm -rf venv
