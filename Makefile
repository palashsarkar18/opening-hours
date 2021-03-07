run:
	FLASK_ENV=development FLASK_APP=standings/main.py flask run

test:
	pytest

lint:
	flake8