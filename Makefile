run:
	FLASK_ENV=development FLASK_APP=restaurant/main.py flask run

test:
	pytest

lint:
	flake8