venv:
	python3 -m virtualenv -p $(shell which python3) ./venv
	bash -c 'source ./venv/bin/activate; python3 -m pip install -r requirements.txt'
	bash -c 'source ./venv/bin/activate; python3 -m pip install -r requirements.dev.txt'

update-venv:
	bash -c 'source ./venv/bin/activate; python3 -m pip install -r requirements.txt --upgrade'
	bash -c 'source ./venv/bin/activate; python3 -m pip install -r requirements.dev.txt --upgrade'


tests:
	bash -c 'source ./venv/bin/activate; pytest tests'

.env:
	cp .env.example .env

.PHONY: tests update-venv
