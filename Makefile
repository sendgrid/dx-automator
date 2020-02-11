.PHONY: install clean

venv:
	python3 -m venv venv

install: venv
	. venv/bin/activate; pip install -r requirements.txt

clean:
	rm -rf venv
